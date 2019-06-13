import xadmin
from .models import *


class PassengerAdmin(object):
    list_display = ('username', 'real_name', 'sex', 'card_id', 'register_date')
    search_fields = ('username', 'real_name', 'sex', 'card_id', 'register_date')


xadmin.site.register(Passenger, PassengerAdmin)


class FlightLineAdmin(object):
    list_display = ('flight', 'start_city', 'arrive_city', 'start_airport', 'arrive_airport', 'leave_date', 'leave_time',
                    'arrive_time', 'fly_time', 'business_price', 'tourist_price', 'already_sale', 'for_sale')
    search_fields = ('flight', 'start_city', 'arrive_city', 'start_airport', 'arrive_airport', 'leave_date',
                     'leave_time', 'arrive_time', 'business_price', 'tourist_price')


xadmin.site.register(FlightLine, FlightLineAdmin)


class FlightAdmin(object):
    list_display = ('flight_number', 'flight_name', 'business_class', 'tourist_class')
    search_fields = ('flight_number', 'flight_name')


xadmin.site.register(Flight, FlightAdmin)


class OrderAdmin(object):
    list_display = ('flight_line', 'passenger', 'cabin', 'is_back', 'create_time')
    search_fields = ('flight_line', 'passenger', 'cabin', 'is_back')


xadmin.site.register(Order, OrderAdmin)
