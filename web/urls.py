
from django.urls import path

from web.views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('index/', index, name='index'),
    path('search_result/', search_result, name='search'),
    path('order/<int:line_id>/', order, name='order'),
    path('p_order/', p_order, name='p_order'),
    path('fail_order/', fail_order, name='f_order'),
    path('back_ticket/<int:order_id>/', back_ticket, name='back'),
    path('p_info/', passenger_info, name='p_info'),
    path('change_password/', change_password, name='change'),
    path('order_info/<int:order_id>/', order_info, name='order_info'),
    path('forget/', forget_password, name='forget'),
]
