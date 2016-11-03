from django.conf.urls import url 
from myweb.views import user_info_handler, user_order_handler, user_site_handler, post_addr_handler, session_input

urlpatterns = [
    url(r'user_center_info/$', user_info_handler, name = 'user_info_handler'),
    url(r'user_center_oder([0-9]*)/$', user_order_handler, name = 'user_oder_handler'),
    url(r'user_center_site/$', user_site_handler, name = 'user_site_handler'),
    url(r'post_addr_handler/$', post_addr_handler, name = 'post_addr_handler'),
    url(r'put/$', session_input)
]