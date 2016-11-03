from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.seseklns.backends.db import SessionStore

def login_required(func):
    def wrapper(request, *args, **argv):
        user = request.session.get('uname', default='')
        
        if user:
            dic = {
                'uname': user,           
            }
            return func(request, dic, *args, **argv)
        redirect = HttpResponseRedirect('/login')
        return redirect
    return wrapper

def record_goods(func):
    def wrapper(request, id, *args, **argv):
        sessionList = request.session.get('recentRead')
        if sessionList:
            sessionLength = len(sessionList)
            
            if sessionLength > 4:
                sessionList.pop()
                sessionList.insert(0,id)
                request.session['recentRead'] = sessionList

            elif sessionLength < 4 and sessionLength > 0:
                sessionList.append(id)
                request.session['recentRead'] = sessionList
        else:
            readList = []
            readList.append(id)
            request.session['recentRead'] = readList

        return func(request, id, *args, **argv)
    return wrapper

# from email.mime.base import MIMEBase
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
# from email.utils import parseaddr,formataddr
# from email.header import Header
# from email.encoders import encode_base64
# msg = MIMEMultipart()


# def _format_addr(s):
#     name,addr = parseaddr(s)
#     return formataddr((Header(name,'utf-8').encode(),addr))

# smtp_sever = 'smtp.qq.com'
# from_addr = ''#input('From:')
# password = ''#input('Pass Word:')

# to_addr = ''#input ('to:')#

# msg.attach(MIMEText('hello,send by ...','plain','utf-8'))

# with open('/Users/wangye/Desktop/bg3.png','rb') as f:
#     mime = MIMEBase('image','png',filename ='bg3.png')
#     mime.add_header('content-Disposition','attachment',filename = 'bg3.png')
# # input('STMP sever:')
#     mime.add_header('Content-id','<0>')
#     mime.add_header('X-attachment-Id','0')

#     mime.set_payload(f.read())
#     encode_base64(mime)
#     msg.attach(mime)

# msg['From']  = _format_addr('Python_admin <%s>' % from_addr)
# msg['to'] =  _format_addr('admin <%s>'  % to_addr)
# msg['Subject'] = Header('From STMP ...','utf-8').encode()



# try:

#     smtp_port = 465
#     server = smtplib.SMTP_SSL(smtp_sever,smtp_port)
#     #server.starttls()
#     server.set_debuglevel(1)
#     server.login(from_addr,password)
#     server.sendmail(from_addr,[to_addr],msg.as_string())
#     server.quit()
# except smtplib.SMTPException as e:
#     print('Fail',e)
