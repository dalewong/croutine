from django.shortcuts import render
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator
#from web_util_tool import login_required
def session_input(request):
    sessionList = request.session['rencentRead']
    sessionLength = length(sessionList)
    if sessionLength > 4:
        sessionList.pop()
        sessionList.insert(0,1)
    elif sessionLength < 4 and sessionLength > 0:
        sessionList.append(1)
    else:
        readList = []
        readList.append(1)
        readList.append(2)
        request.session['recentRead'] = readList

    return HttpResponse(' already write ')


#@login_required
def user_info_handler(request):
     
    #user_name = request.session.get('name')
    #user = User_db.objects.filter(user_name = user_name)
    user = User_db.objects.get(pk = 1)
    readList = request.session.get('recentRead')
    goodsList = []
    print(goodsList)
    if readList:
        for id in readList:
            goods = Goods_info.objects.get(pk = id)
            goodsList.append(goods)

    dic = {
        'user': user,
        'goodsList': goodsList
    }

    return render(request, 'user_center_info.html', dic)

#@login_required
def user_order_handler(request, pIndex):
#     user_name = request.session.get('name')
#     user = User_db.objects.filter(user_name = user_name)
    user = User_db.objects.get(pk = 1)
    order_list_all = user.ord_set.all()
    if pIndex == '':
        pIndex = 1
    p = Paginator(order_list_all,2)
    pIndex = int(pIndex)
    range = p.page_range[:6]
    order_list = []
    max = range[-1]
    if pIndex > max:
        order_list = p.page(max)
    elif pIndex < 1:
        order_list = p.page(1)
    else:
        order_list = p.page(pIndex)
    
    dic = {
     'order_list' : order_list,
     'pRange': range,
     'pIndex': pIndex,
     'pMax' : range[-1]
    }
    return render(request, 'user_center_oder.html', dic)

#@login_required
def user_site_handler(request):
#     user_name = request.session.get('name')
#     user = User_db.objects.filter(user_name = user_name)
    user = User_db.objects.get(pk = 1)    
    receiver = user.receiver_set.all()
    
    dic = {'receiver': receiver}
    
    return render(request, 'user_center_site.html', dic)

def post_addr_handler(request):
#   user_name = request.session.get('name')
#   user = User_db.objects.filter(user_name = user_name)
    user = User_db.objects.get(pk = 1) 
    name = request.POST['receiver_name']
    addr = request.POST['receiver_address']
    zipcode = request.POST['receiver_zipcode']
    phone_num = request.POST['receiver_phone']
    mark = 0
    writable = True
    for recv in user.receiver_set.all() :
        print(request.POST)
        if str(recv.id) in request.POST:
            writable = False
            recv.receiver_address = addr
            recv.receiver_name = name
            recv.receiver_phone = phone_num
            recv.receiver_email = zipcode

            recv.save()
    if writable:
        r = Receiver()
        r.receiver_address = addr
        r.receiver_name = name
        r.receiver_phone = phone_num
        r.receiver_email = zipcode
        r.receiver_user_id = user
        r.save()

    return HttpResponseRedirect('/user_center_site')













