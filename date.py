# -*- coding:utf-8 -*-
#将用户输入的数字转化为时间
months=[
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
    ]
#日期以 1 2 3结尾
endings=['st','nd','rd']+17*['th']+['st','nd','rd']+7*['th']+['st']

year = raw_input("year:")
month = raw_input("month:")
day = raw_input("day:")

month_num = int(month)
day_num = int(day)

print day + endings[day_num-1] +" "+ months[month_num-1] +" "+ year


