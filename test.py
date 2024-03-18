from datetime import datetime
import random
from colorama import Fore
from dateutil.relativedelta import relativedelta
import time
import os

import os
import math
import numpy as np
import statistics as s
import matplotlib.pyplot as plt

from colorama import Fore
from utils import col_txt
from collections import Counter
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from dateutil.relativedelta import relativedelta
from data import im_date, ped, course, t_data, e_data, pred_ped

'''
# ! date minus
first_day=int(input("Day: "))
first_month=int(input("Month: "))
first_year=int(input("Year: "))
print('')

second_day=int(input("Day: "))
second_month=int(input("Month: "))
second_year=int(input("Year: "))
print('')

first_date=datetime(first_year, first_month, first_day)
second_date=datetime(second_year, second_month, second_day)

diff=relativedelta(second_date, first_date)
print('')
print(f'The diff is:\n{diff.years} years, {diff.months} months, {diff.days} days\nor {(second_date-first_date).days} days')
print('')

'''

'''
# ! random 
print('Type in your option')
options = [
    'pho bo',
    'bun bo',
    'banh gio',
    'bun ca',
    'bun dau',
    'bun rieu',
    'pho ngan dem',
]
is_using_default_options=True if input('Default?')=='1' else False

if is_using_default_options == False:
    options=[]

while True:
    option = input()
    if option=='':
        break
    else:
        options.append(option)

random_number = random.randint(0, len(options)-1)
print(options[random_number])
'''

ped_list = ped + [datetime.now()]
c_list = course

result_list=[]
circles=[]
values=[]

for i in range(len(ped_list)-1):
    course_circle = [c_date for c_date in c_list if c_date >= ped_list[i] and c_date < ped_list[i+1]]
    course_circle_count=len(course_circle)
    result_list.append([ped_list[i], ped_list[i+1], course_circle_count])

    values.append(course_circle_count)
    circles.append(f'{ped_list[i].strftime("%m/%y")}')

for item in result_list:
    previous_p=item[0].strftime("%d/%m/%y")
    following_p=item[1].strftime("%d/%m/%y")
    count=item[-1]
    print(f'{previous_p} - {following_p}: {count}')

mean = s.mean([item[-1] for item in result_list])
print(f'AVG: {round(mean, 2)}')

plt.figure(figsize=(5, 3))
plt.bar(circles, values, color='skyblue')
plt.grid(axis='y', linestyle='--', alpha=0.7, which= 'both')
plt.xlabel('Month')
plt.ylabel('Count')
plt.title('Course / Ped')
plt.show()