from django.db import models


class Passenger(models.Model):
    SEX = (
        (1, '男'),
        (0, '女')
    )
    username = models.CharField(verbose_name='用户名', max_length=10, unique=True, null=False)
    real_name = models.CharField(verbose_name='乘客姓名', max_length=10, null=False)
    password = models.CharField(max_length=255, null=False)
    register_date = models.DateField(verbose_name='注册时间', null=False, auto_now_add=True)
    sex = models.IntegerField(choices=SEX, verbose_name='性别', null=False)
    card_id = models.CharField(verbose_name='身份证号', max_length=18, null=False)

    class Meta:
        db_table = 'passenger'
        verbose_name = '乘客信息'
        verbose_name_plural = '乘客信息'

    def __str__(self):
        return self.real_name


class Flight(models.Model):
    flight_number = models.CharField(max_length=10, verbose_name='航班号')
    flight_name = models.CharField(max_length=100, verbose_name='航班名')  # 班次  春秋航空9C8995
    business_class = models.IntegerField(default=0, verbose_name='商务舱座位数')
    tourist_class = models.IntegerField(default=0, verbose_name='经济舱座位数')

    class Meta:
        db_table = 'flight'
        verbose_name = '飞机信息'
        verbose_name_plural = '飞机信息'

    def __str__(self):
        return self.flight_name + self.flight_number


class FlightLine(models.Model):
    start_city = models.CharField(max_length=10, null=True, verbose_name='出发城市')
    arrive_city = models.CharField(max_length=10, null=True, verbose_name='到达城市')
    start_airport = models.CharField(max_length=10, null=True, verbose_name='起飞机场')
    arrive_airport = models.CharField(max_length=10, null=True, verbose_name='到达机场')
    leave_date = models.DateField(null=True, verbose_name='出发日期')
    leave_time = models.DateTimeField(null=True, verbose_name='出发时间')
    arrive_time = models.DateTimeField(null=True, verbose_name='到达时间')
    fly_time = models.TimeField(null=True,  verbose_name='飞行时长')
    business_price = models.DecimalField(null=True, max_digits=5, decimal_places=1, verbose_name='商务舱价格')
    tourist_price = models.DecimalField(null=True, max_digits=5, decimal_places=1, verbose_name='经济舱价格')
    for_sale = models.IntegerField(null=True, verbose_name='剩余数量')
    already_sale = models.IntegerField(null=True, default=0,  verbose_name='已售数量')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, verbose_name='乘坐飞机')

    class Meta:
        db_table = 'flight_line'
        verbose_name = '航线信息'
        verbose_name_plural = '航线信息'

    def __str__(self):
        return self.flight.flight_name + self.flight.flight_number + '(' + str(self.leave_date) + ' ' + str(self.leave_time) + ')'


class Order(models.Model):
    Status = (
        (1, '已订票'),
        (0, '已退票')
    )
    Cabin = (
        (1, '经济舱'),
        (2, '商务舱')
    )
    cabin = models.IntegerField(choices=Cabin, null=True, verbose_name='乘坐舱位')
    flight_line = models.ForeignKey(FlightLine, on_delete=models.CASCADE, null=True, verbose_name='乘坐航班')
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, null=True, verbose_name='乘客')
    is_back = models.IntegerField(choices=Status, null=True, default=1, verbose_name='状态')
    create_time = models.DateTimeField(null=True, auto_now=True)

    class Meta:
        db_table = 'order'
        verbose_name = '订单信息'
        verbose_name_plural = '订单信息'


