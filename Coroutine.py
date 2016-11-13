from queue import Queue
from abc import abstractmethod
from select import select

#task
class Task(object):
    taskid = 0  #every task should has an unique id
    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target  #run coroutine
        self.sendval = None

    def run(self):
        return self.target.send(self.sendval)

#cpu
class Scheduler(object):
    def __init__(self):
        self.ready = Queue()  #task queue init
        self.taskmap = {}  #local task
        self.exit_waiting = {}
        self.read_waiting = {}
        self.write_waiting = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.tid] = newtask
        self.schedule(newtask)
        return newtask.tid

    def schedule(self, task):
        self.ready.put(task)

    def mainloop(self):  #main loop seems like cpu
        self.new(self.iotask())  #开启select
        while self.taskmap:
            task = self.ready.get()
            try:
               result = task.run()
               #os
               if isinstance(result,SystemCall):  #use system call to give control back to os(this seems like trap)
                   result.task = task
                   result.sched = self
                   result.handle()  #back to os hook
               #################################
                   continue

            except StopIteration:
                self.exit(task)
                continue
            self.schedule(task)

    def exit(self, task):  #task exit func
        print('Task %d terminiated' % task.tid)
        print(task.tid)

        del self.taskmap[task.tid]  #del task map
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)  #close all task

    def waitforexit(self, task, waittid): #task wait for exit func
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid,[]).append(task)
            return True
        else:
            return False

    def waitforread(self, task, fd):  #register to os
        self.read_waiting[fd] = task

    def waitforwrite(self, task, fd):  #register to os
        self.write_waiting[fd] = task

    def iopoll(self, timeout):
        #select

        if self.read_waiting or self.write_waiting:
            #write_wait = self.write_waiting.keys()
            #read_wait = self.read_waiting.keys()
            r, w, e = select(self.read_waiting,
                             self.write_waiting,[],timeout)

            for fd in r:
                self.schedule(self.read_waiting.pop(fd))  #add to task

            for fd in w:
                self.schedule(self.write_waiting.pop(fd))  #add to task

    def iotask(self):  #use select
        while True:
            if self.ready.empty():
                self.iopoll(None)  #no data to write and read
            else:
                self.iopoll(0)  #have data -> run forever
            yield

#os
class SystemCall(object):
    @abstractmethod
    def handle(self):
        pass

#get task id
class GetTid(SystemCall):
    def handle(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)

#create new task
class NewTask(SystemCall):
    def __init__(self, target):
        self.target = target

    def handle(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)

#close a task
class KillTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        task = self.sched.taskmap.get(self.tid,None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False

        self.sched.schedule(self.task)


class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handle(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result

        if not result:
            self.sched.schedule(self.task)


class ReadWait(SystemCall):
    def __init__(self, f):
        self.f = f
    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforread(self.task,fd)
        #self.sched.schedule(self.task)


class WriteWait(SystemCall):
    def __init__(self,f):
        self.f = f
    def handle(self):
        fd = self.f.fileno()
        self.sched.waitforwrite(self.task,fd)

#server
from socket import *

def handle_client(client, addr):
    print('connection from {}'.format(addr))
    while True:
        print('ready to read client-------')
        yield ReadWait(client)
        data = client.recv(1024)
        if not data:
            break
        print('ready to write client--------')
        yield WriteWait(client)
        client.send(data)
        print('client ready to close')

    client.close()
    print('Client closed')
    yield  #this may be important cus use this to break back control to os

def server(port):
    print('Server starting')
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('',port))
    sock.listen(5)
    while True:
        print('ready read-----')
        yield ReadWait(sock)
        client, addr = sock.accept()
        print('ready create new task----')
        yield NewTask(handle_client(client,addr))

#def alive():
    # while True:
    #     print('i am alive')
    #     yield

sched = Scheduler()
#sched.new(alive())
sched.new(server(4455))
sched.mainloop()