# -*- coding:utf-8 -*-
from __future__ import unicode_literals

def convert_time(time):
    try:
        hour = int(time.split(':')[0])
        minute = time.split(':')[1]
    except:
        hour = 0
        minute = '00'
    period = 'AM'
    if hour == 0: # midnight
        hour = 12
    elif hour >= 12:
        hour = hour - 12
        period = 'PM'
    hour = str(hour)
    time = {'hour':hour,'minute':minute,'period':period}
    return time

def revert_time(hour,minute,period):
    if period == 'PM':
        hour = str(int(hour) + 12)
    elif period == 'AM' and hour == '12':
        hour = 0
    time = str(hour) + ':' + minute
    return time
    