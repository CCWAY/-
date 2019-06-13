from datetime import datetime
from operator import attrgetter

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from web.forms import PassengerForm
from web.forms_login import LoginForm
from web.forms_search import SearchForm
from web.models import Passenger, FlightLine, Order


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 定义表单，验证页面传递的参数
        form = PassengerForm(request.POST)
        if form.is_valid():
            # 获取数据并校验
            # 校验成功
            # form.cleaned_data 取值
            Passenger.objects.create(username=form.cleaned_data['username'],
                                     real_name=form.cleaned_data['real_name'],
                                     password=make_password(form.cleaned_data['password']),
                                     sex=form.cleaned_data['sex'],
                                     card_id=form.cleaned_data['card_id'],
                                     )
            return HttpResponseRedirect(reverse('web:login'))

        errors = form.errors
        return render(request, 'register.html', {'errors': errors})


# 用户登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 登录操作
            passenger = Passenger.objects.filter(username=form.cleaned_data['username']).first()
            request.session['user_id'] = passenger.id
            url = request.session['url']
            if url == '/web/index/':
                return HttpResponseRedirect(reverse('web:index'))
            if url == '/web/search_result/':
                return HttpResponseRedirect(reverse('web:search'))

        errors = form.errors
        return render(request, 'login.html', {'errors': errors})


# 忘记密码
def forget_password(request):
    if request.method == 'GET':
        return render(request, 'forget_password.html')

    if request.method == 'POST':
        username = request.POST.get('username')
        real_name = request.POST.get('real_name')
        card_id = request.POST.get('card_id')
        password = request.POST.get('new_password')
        user = Passenger.objects.get(username=username)
        if not user.username == username:
            error = '用户名不存在'
            return render(request, 'forget_password.html', {'error': error})
        if not user.real_name == real_name:
            error = '真实姓名输入不符'
            return render(request, 'forget_password.html', {'error': error})
        if not card_id == user.card_id:
            error = '身份证号有误'
            return render(request, 'forget_password.html', {'error': error})
        if 5 < len(password) < 17:
            password = make_password(password)
            user.password = password
            user.save()
            return HttpResponseRedirect(reverse('web:login'))
        error = '密码不符合规范（在6到16位之间）'
        return render(request, 'forget_password.html', {'error': error})


# 注销
def logout(request):
    request.session['user_id'] = None
    return HttpResponseRedirect(reverse('web:index'))


# 主页，查询机票
def index(request):
    if request.method == 'GET':
        url = request.path
        request.session['url'] = url
        if 'user_id' in request.session:
            if request.session.get('user_id', None) is not None:
                user = Passenger.objects.get(pk=request.session['user_id'])
                return render(request, 'index.html', {'user': user})
        return render(request, 'index.html', {'user': None})

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            s_city = request.POST.get('start_city')
            a_city = request.POST.get('arrive_city')
            leave_date = request.POST.get('leave_date')
            request.session['s_city'] = s_city
            request.session['a_city'] = a_city
            request.session['leave_date'] = leave_date
            return HttpResponseRedirect(reverse('web:search'))
        errors = form.errors
        return render(request, 'index.html', {'errors': errors})


# 　查询结果
def search_result(request):
    if request.method == 'GET':
        url = request.path
        request.session['url'] = url
        lines = FlightLine.objects.all()
        for line in lines:
            line.for_sale = (line.flight.business_class + line.flight.tourist_class) - line.already_sale
            line.save()
        s_city = request.session['s_city']
        a_city = request.session['a_city']
        leave_date = request.session['leave_date']
        l_date = datetime.strptime(leave_date, '%Y-%m-%d').date()
        flight_lines = FlightLine.objects.filter(leave_date=l_date,
                                                 start_city=s_city,
                                                 arrive_city=a_city).all()
        lines = []
        for flight_line in flight_lines:  # off-set aware
            lines.append(flight_line)

        # 按起飞的时间排序
        usable_flights_by_ltime = sorted(lines, key=attrgetter('leave_time'))  # 起飞时间从早到晚
        # 按价格进行排序
        usable_flights_by_price = sorted(lines, key=attrgetter('tourist_price'))  # 起飞时间从早到晚
        user_id = request.session.get('user_id', None)
        if not lines:
            error = 'block'
            if user_id is None:
                context = {
                    'start_city': s_city,
                    'arrive_city': a_city,
                    'leave_date': leave_date,
                    'user':  None
                }
                return render(request, 'result.html', context, {'error': error})
            else:
                context = {
                    'start_city': s_city,
                    'arrive_city': a_city,
                    'leave_date': leave_date,
                    'user': Passenger.objects.get(pk=user_id)
                }
                return render(request, 'result.html', context, {'error': error})
        error = 'none'
        if user_id is None:
            context = {'lines': lines,
                       'error': error,
                       'usable_flights_by_ltime': usable_flights_by_ltime,
                       'usable_flights_by_price': usable_flights_by_price,
                       'start_city': s_city,
                       'arrive_city': a_city,
                       'leave_date': leave_date,
                       'user': None
                       }
            return render(request, 'result.html', context)
        else:
            context = {'lines': lines,
                       'error': error,
                       'usable_flights_by_ltime': usable_flights_by_ltime,
                       'usable_flights_by_price': usable_flights_by_price,
                       'start_city': s_city,
                       'arrive_city': a_city,
                       'leave_date': leave_date,
                       'user': Passenger.objects.get(pk=user_id)
                       }
            return render(request, 'result.html', context)

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            s_city = request.POST.get('start_city')
            a_city = request.POST.get('arrive_city')
            leave_date = request.POST.get('leave_date')
            request.session['s_city'] = s_city
            request.session['a_city'] = a_city
            request.session['leave_date'] = leave_date
            return HttpResponseRedirect(reverse('web:search'))
        errors = form.errors
        return render(request, 'index.html', {'errors': errors})


# 订票
def order(request, line_id):
    if request.method == 'GET':
        if request.session.get('user_id', None) is None:
            error = 'block'
            return render(request, 'order.html', {'error': error, 'success': 'none'})
        user = Passenger.objects.get(pk=request.session['user_id'])
        line = FlightLine.objects.get(pk=line_id)
        orders = Order.objects.filter(passenger_id=request.session['user_id']).all()
        for order in orders:
            if order.flight_line == line and order.is_back == 1:
                error2 = '你已经预定过此航班, 不能重复进行订票！'
                return render(request, 'order.html', {'error': 'block', 'error2': error2, 'success': 'none'})
        line.already_sale += 1
        line.save()
        return render(request, 'order.html', {'line': line, 'user': user, 'error': 'none', 'success': 'block'})

    if request.method == 'POST':
        Order.objects.create(passenger_id=request.session['user_id'],
                             flight_line_id=line_id,
                             cabin=request.POST['cabin']
                             )
        return HttpResponseRedirect(reverse('web:p_order'))


# 可出行订单列表
def p_order(request):
    if request.method == 'GET':
        order_list = Order.objects.filter(passenger_id=request.session.get('user_id', None)).all()
        user_id = request.session.get('user_id', None)
        user = Passenger.objects.get(pk=user_id)
        if order_list:
            error = 'block'
            for order in order_list:
                if order.is_back == 1:
                    error = 'none'
            return render(request, 'p_orders.html', {'orders': order_list, 'error': error, 'user': user})
        error = 'block'
        return render(request, 'p_orders.html', {'error': error, 'user': user})


# 退票
def back_ticket(request, order_id):
    if request.method == 'GET':
        back_order = Order.objects.get(pk=order_id)
        back_order.is_back = 0
        back_order.flight_line.already_sale -= 1
        back_order.flight_line.save()
        back_order.save()
        return HttpResponseRedirect(reverse('web:p_order'))


# 历史订单
def fail_order(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id', None)
        user = Passenger.objects.get(pk=user_id)
        order_list = Order.objects.filter(passenger_id=request.session.get('user_id', None)).all()
        if order_list:
            error = 'block'
            for order in order_list:
                if order.is_back == 0:
                    error = 'none'
            return render(request, 'f_orders.html', {'orders': order_list, 'error': error, 'user': user})
        error = 'block'
        return render(request, 'f_orders.html', {'error': error, 'user': user})


# 乘客个人信息
def passenger_info(request):
    if request.method == 'GET':
        p_info = Passenger.objects.get(pk=request.session.get('user_id', None))
        return render(request, 'passenger_info.html', {'info': p_info})

    if request.method == 'POST':
        username = request.POST['username']
        real_name = request.POST['real_name']
        card_id = request.POST['card_id']
        sex = request.POST['sex']
        passenger = Passenger.objects.get(pk=request.session.get('user_id', None))
        passenger.username = username
        passenger.real_name = real_name
        passenger.card_id = card_id
        passenger.sex = sex
        passenger.save()
        passenger = Passenger.objects.get(pk=request.session.get('user_id', None))
        return render(request, 'passenger_info.html', {'info': passenger})


# 修改密码
def change_password(request):
    if request.method == 'GET':
        return render(request, 'change_password.html')

    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        passenger = Passenger.objects.get(pk=request.session.get('user_id', None))
        if not check_password(old_password, passenger.password):
            error = '你的密码输入有误，请重新输入'
            return render(request, 'change_password.html', {'message': error})
        passenger.password = make_password(new_password)
        passenger.save()
        success = '修改密码成功'
        return render(request, 'change_password.html', {'message': success})


# 订单详情
def order_info(request, order_id):
    if request.method == 'GET':
        order = Order.objects.get(pk=order_id)
        return render(request, 'order_info.html', {'order': order})



