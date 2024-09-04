import os
import math
import numpy as np
import pandas as pd
import statistics as s
import matplotlib.pyplot as plt

from prettytable import PrettyTable

from colorama import Fore
from utils import col_txt, logger
from collections import Counter
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
from dateutil.relativedelta import relativedelta
from lunarcalendar import Converter, Solar, Lunar, DateNotExist
from data import im_date, ped, course, t_data, e_data, pred_ped, remains, save_goal, tkb, period

def sol_to_lu_date(date: datetime):
    solar=Solar(date.year, date.month, date.day)
    lunar=Converter.Solar2Lunar(solar)
    return lunar

def sol_to_lu_dates(list_date: list[datetime]):
    for date in list_date:
        solar=Solar(date.year, date.month, date.day)
        lunar=Converter.Solar2Lunar(solar)
        lunar_color= Fore.LIGHTGREEN_EX if lunar.day==1 else Fore.RESET
        lunar_log=lunar_color+f'{lunar.day}/{lunar.month}/{lunar.year}'+Fore.RESET
        print(f'{solar.day}/{solar.month}/{solar.year} -> ' + lunar_log)
    print('===')

def get_total(source = 't'or 'e' or 'i' or 's' or None, is_q: bool = False):
    if source!=None:
        if is_q:
            return sum([m[1] for m in remains if m[2] == source if m[3]!='p'])
        else:
            return sum([m[1] for m in remains if m[2] == source ])
    else:
        if is_q:
            return sum([m[1] for m in remains if m[3]!='p'])
        else:
            return sum([m[1] for m in remains])
        
def get_positive_total():
    return sum([m[1] for m in remains if m[2] != 's' ])

def get_crochet_total():
    return sum([m[1] for m in remains if m[2] == 'e' and m[3] == 'p'])
    
def get_values(source: str):
    if source == '1':
        
        values = [t[1] for t in remains if t[3] == 't']
    elif source == '2':
        values = [t[1] for t in remains if t[3] == 'e']
    elif source == '3':
        values = [t[1] for t in remains if t[3] == 'i']
    else:
        values = [t[1] for t in remains]
    return values

def predict_drop(x, x1, y1, slope):
    result = int(slope * (x - x1) + y1)
    return result

def value_change(values: list, dates: list, log: str='', is_max: bool=True):
    current_mean_raw=values[-1]
    current_mean_rounded=round(current_mean_raw, 2)
    current_date=dates[-1]

    value_to_compare=0
    date=datetime.now()

    if is_max==True:
        max_value=max(values)
        max_index = len(values) - values[::-1].index(max_value) - 1

        # max_index=values.index(max(values))
        value_to_compare=values[max_index]
        date=dates[max_index]
    else:
        value_to_compare=values[0]
        date=dates[0]
    
    value_to_compare_round=round(value_to_compare, 2)
    change = round(current_mean_raw*100/value_to_compare-100, 2)

    log=log
    color = Fore.GREEN if change >=0 else Fore.RED
    sign_prefix='+' if change >= 0 else ''
    
    diff=(current_date-date).days
    log+=col_txt(color, f' {current_mean_rounded}') 
    log+=f'/{value_to_compare_round} (' + col_txt(color, f'{sign_prefix}{change}%') 
    log+=f' in {diff} days)'
    print(log)

def is_this_good(previous_ped, course_date, follow_ped):
    course_date_format = course_date.strftime("%d/%m/%y")
    lunar_date=sol_to_lu_date(course_date)
    lunar_date_format=f'{lunar_date.day}/{lunar_date.month}/{lunar_date.year}'
    lunar_text=col_txt(Fore.LIGHTYELLOW_EX if lunar_date.day==1 else Fore.BLACK, f'[{lunar_date_format}]')

    print(col_txt(Fore.BLACK,'-----\n')+f'{course_date_format}  {lunar_text}:')

    if previous_ped is not None:
        dif=(course_date-previous_ped).days+1
        color = Fore.LIGHTGREEN_EX if dif >= 20 else Fore.LIGHTRED_EX
        ped_date_format=previous_ped.strftime("%d/%m/%y")
        print(col_txt(Fore.LIGHTBLACK_EX, ' (p) ') + col_txt(color, f'{ped_date_format}: ({dif})'))

    if follow_ped is not None:
        dif=(follow_ped-course_date).days
        color = Fore.LIGHTGREEN_EX if dif <=10 else Fore.LIGHTRED_EX
        ped_date_format=follow_ped.strftime("%d/%m/%y")
        print(col_txt(Fore.LIGHTBLACK_EX, ' (f) ') + col_txt(color, f'{ped_date_format}: ({dif})'))

def find_y(x1, x2, y1, y2, given_x):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m * given_x + b     

def find_y_by_time(x1: datetime, x2: datetime, y1, y2, given_x: datetime):
    return find_y(x1.timestamp(), x2.timestamp(), y1, y2, given_x.timestamp())    

def number_to_ordinal(number):
    number = int(number)
    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')
    return str(number) + suffix

class soft_function:
    # ! Change percent calcu
    def change_percent_cal(title: str = None, is_plot: bool = False):
        start_date=datetime.now()
        try:
            list=[]
            if title=='T data':
                list=t_data
            elif title=='E data':
                list=e_data
            else:
                return
            list_mean= [s.mean(item[0]) for item in list]
            list_date= [item[1] for item in list]

            first_date: datetime=list_date[0]
            first_date_formatted=first_date.strftime("%d/%m/%y")
            print(col_txt(Fore.LIGHTWHITE_EX, f'{title} (start from {first_date_formatted}):'))

            for i in range(0, len(list)-1):
                before_mean=list_mean[i]
                after_mean=list_mean[i+1]
                
                before_date: datetime=list_date[i]
                after_date: datetime=list_date[i+1]
                distance_in_day=(after_date-before_date).days

                change_percent = after_mean*100/before_mean-100

                sign_prefix = ''
                if change_percent >-10 and change_percent <0:
                    sign_prefix = ' '
                if change_percent>=0 and change_percent <10:
                    sign_prefix = ' +'
                if change_percent >= 10:
                    sign_prefix = '+'
                
                after_date=after_date.strftime("%d/%m")
                color=Fore.GREEN if change_percent>=0 else Fore.RED
                min_max_indicator=Fore.BLACK
                if after_mean == min(list_mean):
                    min_max_indicator=Fore.LIGHTRED_EX
                if after_mean == max(list_mean):
                    min_max_indicator=Fore.LIGHTGREEN_EX
                
                log=''
                log+=col_txt(Fore.WHITE, f'[{after_date}]')
                log+=col_txt(Fore.BLACK, f'\t~{distance_in_day} d:\t') 
                log+=col_txt(color, f'{sign_prefix}{round(change_percent, 2)}%') 
                log+=col_txt(min_max_indicator, f'\t({round(after_mean, 2)})')
                print(log)

            print('------------------------')
            value_change(dates=list_date, is_max=False, log='Current/Begining (10):', values=list_mean)
            value_change(dates=list_date, is_max=True, log='Current/ATH (10): ', values=list_mean)

            # Predict
            x1=list_mean[0]
            x2=list_mean[1]
            y1=0
            y2=(list_date[1]-list_date[0]).days
            slope=(y2 - y1) / (x2 - x1)
            days=predict_drop(slope=slope,x1=x1, y1=y1, x=0)
            drop_day=list_date[-1]+timedelta(days=days)
            print(f'{title} will likely drop to 0 by ' + col_txt(Fore.CYAN, f'[{drop_day.strftime("%d/%m/%y")}]') + f' ({days} days)\n')

            # Plotting
            if is_plot==True:
                plt.ioff()
                plt.figure(figsize=(5, 3))  
                plt.plot(list_date, list_mean, marker='o', color='blue', linestyle='-')  
                last_x = list_date[-2:]
                last_y = list_mean[-2:]
                plt.scatter(drop_day, 0, color='red')
                plt.plot(last_x, last_y, color='blue', linestyle='-')

                plt.title(title if title != None else 'Dummy') 
                plt.xlabel('Date')  
                plt.ylabel('Mean')  
                plt.grid(True) 
                plt.tight_layout()
                plt.xticks(rotation=45)
                plt.show()
    
        except Exception as e:
            logger.error(e)

        end_date=datetime.now()
        if is_plot==False:
            print(col_txt(Fore.LIGHTBLACK_EX, f"Process in {(end_date-start_date).microseconds} microsec"))

    # ! Counting
    def cal_date():
        try:
            now=datetime.now()
            # 
            # is_take_input=False if input('Input date? (Skip= 1)\n')=='1' else True
            # print(col_txt(Fore.BLACK, '-----'))
            # if is_take_input:
            #     day=int(input("Day: "))
            #     month=int(input("Month: "))
            #     year=int(input("Year: "))
            #     now=datetime(year, month, day)
            # 
            last_for=(now-im_date.first_date).days
            last_color = Fore.GREEN if (last_for%100 ==0 or last_for%100==99 or last_for%100==98) else Fore.LIGHTCYAN_EX

            e_y=int((now-im_date.e_BD).days/365)
            t_y=int((now-im_date.t_BD).days/365)

            to_e_BD=datetime(day=im_date.e_BD.day, month=im_date.e_BD.month, year=now.year)
            to_t_BD=datetime(day=im_date.t_BD.day, month=im_date.t_BD.month, year=now.year)

            to_e_BD=(to_e_BD-now).days
            to_t_BD=(to_t_BD-now).days

            if to_e_BD<0:
                to_e_BD=datetime(day=im_date.e_BD.day, month=im_date.e_BD.month, year=now.year+1)
                to_e_BD=(to_e_BD-now).days

            if to_t_BD<0:
                to_t_BD=datetime(day=im_date.t_BD.day, month=im_date.t_BD.month, year=now.year+1)
                to_t_BD=(to_t_BD-now).days

            is_near_e_BD=col_txt(Fore.GREEN, f'{to_e_BD}') if to_e_BD <= 30 else f'{to_e_BD}'
            is_near_t_BD=col_txt(Fore.GREEN, f'{to_t_BD}') if to_t_BD <= 30 else f'{to_t_BD}'

            last_for_rel = relativedelta(now, im_date.first_date)
          
            next_uni = datetime(now.year, now.month, 3)
            if next_uni <= now:
                next_uni += relativedelta(months=1)

            uni_count=relativedelta(next_uni, im_date.first_date).months
            distance=(next_uni-now).days+1

            print('Been for:'+col_txt(last_color,f' {last_for}')+' days')
            if last_for_rel.days==0:
                is_the_day=Fore.LIGHTYELLOW_EX
            else:
                is_the_day=Fore.BLACK
            if last_for_rel.years>0:
                text=f'{last_for_rel.years} years, {last_for_rel.months} months, {last_for_rel.days} days'
            else:
                text=f'{last_for_rel.months} months, {last_for_rel.days} days'

            print(col_txt(is_the_day, text))
            print(col_txt(Fore.BLACK, f'The {number_to_ordinal(uni_count)} uni at {next_uni.strftime("%d/%m/%y")} ({distance} days)'))
            
            print('')
            print(f'Till e {e_y+1} BD: {is_near_e_BD} days ({round(to_e_BD/30, 1)})')
            print(f'Till t {t_y+1} BD: {is_near_t_BD} days ({round(to_t_BD/30, 1)})')
            # dif = relativedelta(im_date.e_BD,im_date.t_BD)
            # print(col_txt(Fore.BLACK, f'Dif: {dif.years} years, {dif.months} months, {dif.days} days'))
            
            
            solar=Solar(now.year, now.month, now.day)
            lunar=Converter.Solar2Lunar(solar)
            lunar_color= Fore.LIGHTGREEN_EX if lunar.day==1 or lunar.day==15 else Fore.RESET
            lunar_log=col_txt(lunar_color, f'{lunar.day}/{lunar.month}/{lunar.year}')
            print(f'\nLunar day: ' + lunar_log)

        except Exception as e:
            logger.error(e)

    # ! Circle
    def pred_pe():
        try:
            date_list: list=ped
            today=datetime.now()

            last_distance=(today-date_list[-1]).days+1
            if last_distance <= 7:
                print(col_txt(Fore.RED, f'Day {last_distance}: It\'s happening'))
            if last_distance > 7 and last_distance < 20:
                print(col_txt(Fore.YELLOW, f'Day {last_distance}: Wait for it! ({20-last_distance})'))
            if last_distance >= 20:
                print(col_txt(Fore.GREEN, f'Day {last_distance}: ALL IN'))

            print(f'{date_list[-1].strftime("%d/%m/%Y")}')

            distances = [(date_list[i+1] - date_list[i]).days for i in range(len(date_list) - 1)]
            mean=round(s.mean(distances), 2)
            print(f'C: {mean} days ' + col_txt(Fore.BLACK, f'{distances} ({date_list[-1].strftime("%d/%m/%Y")})'))

            predict=date_list[-1]+timedelta(days=mean)
            pred_distance=(predict-today).days

            predict_sfa=predict-timedelta(days=10)
            sfa_distance=(predict_sfa-today).days

            if pred_distance<=0:
                print(f'Has it happen? '+col_txt(Fore.LIGHTYELLOW_EX, f'({predict.strftime("%d/%m/%Y")})')+ col_txt(Fore.BLACK, f' ({-pred_distance} days ago)'))
            else:
                print(f'Next c starts at: '+col_txt(Fore.LIGHTYELLOW_EX,f'{predict.strftime("%d/%m/%Y")}')+f' (in {pred_distance})')
                print(f'Nearest sfa: '+col_txt(Fore.BLACK,f'{predict_sfa.strftime("%d/%m/%Y")}')+f' (in {sfa_distance})')

            text_to_find='# pred'
            new_line=f'pred_ped=datetime(day={predict.day}, month={predict.month}, year={predict.year})\n'
            with open('data.py', encoding='utf-8', mode='r') as file:
                lines = file.readlines()
            for i in range (0, len(lines)):
                if text_to_find in lines[i]:
                    lines.pop(i-1)
                    lines.insert(i-1, new_line)
                    break
            with open('data.py', encoding='utf-8', mode='w') as file:
                file.writelines(lines)

        except Exception as e:
            logger.error(e)

    # ! Insert new thing
    def insert_date(select: str=''):
        try:
            is_data=False
            if select != '':
                text_to_find=''
                if select == 'course':
                    text_to_find='# course'
                elif select == 'ped':
                    text_to_find='# ped'
                elif select == 't data':
                    text_to_find='# t data'
                    is_data=True
                elif select == 'e data':
                    text_to_find='# e data'
                    is_data=True
                else: 
                    text_to_find='alsdfkjh!#%$^'
                    
            if is_data == False:
                day=int(input("Day: "))
                month=int(input("Month: "))
                year=int(input("Year: "))

                new_line = f"  datetime(day={day}, month={month}, year={year}),\n"
            else:
                old_data=t_data[-3:] if text_to_find=='# t data' else e_data[-3:]
                for data in old_data:
                    print(col_txt(Fore.BLACK, f'{data[1].strftime("%d/%m/%y")}: ' + col_txt(Fore.LIGHTBLACK_EX, f'{data[0]} ({round(s.mean(data[0]), 2)})')))
                
                com=float(input("Com: "))
                sharing=float(input("Sharing: "))
                lope=float(input("Lope: "))

                day=int(input("Day: "))
                month=int(input("Month: "))
                year=int(input("Year: "))

                new_line = f"  [[{com}, {sharing}, {lope}], datetime(day={day}, month={month}, year={year})],\n"

            is_save=True if input('You really want to save? (yes=1)\n') == '1' else False
            if is_save==True:
                with open('data.py', encoding='utf-8', mode='r') as file:
                    lines = file.readlines()
                for i in range (0, len(lines)):
                    if text_to_find in lines[i]:
                        lines.insert(i-1, new_line)
                        break
                with open('data.py', encoding='utf-8', mode='w') as file:
                    file.writelines(lines)
                print(col_txt(Fore.GREEN,'Done'))
            else:
                print(col_txt(Fore.GREEN, 'Stopped'))

        except Exception as e:
            logger.error(e)

    # ! Plotting stuffs
    def plot_stuffs(ped_date:list = ped, cours_date:list = course):
        try:
            is_continue=True
            while is_continue:
                print('Plotting which?')
                print('- course '+col_txt(Fore.BLACK, '(1)'))
                print('- ped '+col_txt(Fore.BLACK, '(2)'))
                print('- course & ped '+col_txt(Fore.BLACK, '(3)'))
                print('- t data vs e data '+col_txt(Fore.BLACK, '(4)'))
                print('- course & ped vs t data '+col_txt(Fore.BLACK, '(5)'))
                print('- course & ped vs e data '+col_txt(Fore.BLACK, '(6)'))
                chosing=input('- nevermind '+col_txt(Fore.BLACK, '(anything else)\n---\n'))

                if chosing not in ['1', '2', '3', '4', '5', '6']:
                    print('Ok.')
                    break

                print(col_txt(Fore.BLACK, '\nPlotting...'))
                if chosing == '1':
                    # plt.figure(figsize=(5, 3))
                    # plt.plot(cours_date, range(1, len(cours_date)+1), label='Course', marker='o')
                    # plt.plot([datetime.now(), datetime.now()], [0, 10], label='Current Date', marker='X', linestyle='-.')
                    course_per_month = Counter((date.year, date.month) for date in course)

                    month_years = sorted(course_per_month.keys())
                    course_counts = [course_per_month[month_year] for month_year in month_years]

                    plt.figure(figsize=(5, 3))
                    plt.bar(range(len(month_years)), course_counts, color='skyblue', label='per month')
                    plt.xlabel('Date')
                    plt.ylabel('Index')
                    plt.title('Courses data')
                    plt.xticks(range(len(month_years)), [f'{date[1]}/{date[0]}' for date in month_years])
                    plt.grid(axis='y', linestyle='--', alpha=0.7)
                    plt.title('1. Course Plot')
                    
                elif chosing == '2':
                    x_now = datetime.now()
                    y_now = find_y_by_time(ped[-1], pred_ped, 3, 4, x_now)

                    x_safe_day = pred_ped - timedelta(days=10)
                    y_safe_day = find_y_by_time(ped_date[-1], pred_ped, 3, 4, x_safe_day)

                    plt.figure(figsize=(5, 3))
                    plt.plot(ped_date[-3:], range(1, 3+1), label='Ped', marker='o')
                    plt.plot([ped_date[-1], pred_ped], [3, 4], label='Predict Ped', marker='*', linestyle='--')

                    plt.plot([x_now], [y_now], color='red', label='Today', marker='X' )
                    plt.plot([x_safe_day], [y_safe_day], color = 'green', label='safe', marker= '.')

                    plt.xlabel('Date')
                    plt.ylabel('Index')
                    plt.grid(True)
                    plt.xticks(rotation=45)
                    plt.title('2. Ped Plot')

                elif chosing == '3':
                    y_now=find_y_by_time(ped_date[-1], pred_ped, len(ped_date), len(ped_date)+1, datetime.now())
                    y_start=find_y_by_time(ped_date[0], ped_date[1], 1, 2, im_date.first_date)

                    plt.figure(figsize=(5, 3))
                    plt.plot(cours_date, range(1, len(cours_date)+1), label='Course', marker='o')

                    for x in ped_date:
                        plt.plot([x, x], [0, len(cours_date)+1], linestyle='--', color='gray')

                    plt.plot([datetime.now(), datetime.now()], [0, len(cours_date)+1], linestyle='--', color='green')

                    plt.plot(ped_date, range(1, len(ped_date)+1), label='Ped', marker='o')
                    plt.plot([datetime.now()], [y_now], label='Current Date', marker='X', linestyle='-.')
                    plt.plot([im_date.first_date], [y_start], label='First', marker='D', color='purple', linestyle='-.')
                    
                    plt.plot([ped_date[-1], pred_ped], [len(ped_date), len(ped_date)+1], label='Predict Ped', marker='*', linestyle='--')
                    plt.xlabel('Date')
                    plt.ylabel('Index')
                    plt.grid(True)
                    plt.xticks(rotation=45)
                    plt.title('3. Course vs PED Plot')

                elif chosing == '4':
                    change_mean_list_t=[s.mean(item[0]) for item in t_data]
                    change_mean_list_e=[s.mean(item[0]) for item in e_data]
                    change_date_list_t = [item[1] for item in t_data]
                    change_date_list_e = [item[1] for item in e_data]

                    smallest = min(change_mean_list_t+change_mean_list_e)
                    smallest = math.floor(smallest)

                    plt.plot(change_date_list_t, change_mean_list_t, label = 'T data', marker='o', linestyle='-')
                    plt.plot(change_date_list_e, change_mean_list_e, label = 'E data', marker='o', linestyle='--')
                    plt.plot([datetime.now(), datetime.now()], [smallest, 10], label='Current Date', marker='X', linestyle='-.')

                    plt.title('4. T vs E')
                    plt.xlabel('Date')
                    plt.ylabel('Index')                    
                    plt.grid(True)
                    plt.xticks(rotation=45)

                else:
                    is_plotting_data= (chosing == '5' or chosing =='6')
                    if is_plotting_data:
                        change_list = t_data if chosing == '5' else e_data
                        change_date_list = [item[1] for item in change_list]

                        change_mean_list = [s.mean(item[0]) for item in change_list]
                        change_mean_list_reshaped = np.array(change_mean_list).reshape(-1, 1)

                        # sc = MinMaxScaler(feature_range = (1, len(cours_date)+1))
                        sc = MinMaxScaler(feature_range = (1, 10))
                        change_mean_list_scaled=sc.fit_transform(change_mean_list_reshaped)
                        
                    plt.figure(figsize=(5, 3))

                    plt.plot(ped_date, range(1, len(ped_date)+1), label='Ped', marker='o')
                    plt.plot(cours_date, range(1, len(cours_date)+1), label='Course', marker='o')
                    plt.plot([datetime.now(), datetime.now()], [1, 10], label='Current Date', marker='X', linestyle='-.')
                    plt.plot([ped_date[-1], pred_ped], [len(ped_date), len(ped_date)+1], label='Predict Ped', marker='*', linestyle='--')
                    plt.plot([im_date.first_date, im_date.first_date], [0, 10], label='First', marker='D', color='purple', linestyle='-.')

                    title=''
                    if is_plotting_data:
                        plt.plot(change_date_list, change_mean_list_scaled, label='T data' if chosing == '5' else 'E data', marker='o')
                        title = '5. Course Plot T data' if chosing == '5' else '6. Course Plot E data'
                    
                    plt.title(title)
                    plt.xlabel('Date')
                    plt.ylabel('Index')
                    plt.grid(True)
                    plt.xticks(rotation=45)

                plt.legend()

                plt.tight_layout()
                plt.show()

                is_continue=True if input('\n---\nContinue plotting? (yes=1)\n') == '1' else False
                os.system('cls')

        except Exception as e:
            logger.error(e)

    # ! Evaluate course safety
    def evaluate_safety():
        try:
            for each_time in course:
                course_new=[[each_time, 1]]
                ped_new=[[item, 0] for item in ped]
                new_date_list = ped_new + course_new
                new_date_list.sort(key=lambda x: x[0])
                for i in range(0, len(new_date_list)):
                    if new_date_list[i][-1] == 1:
                        p=new_date_list[i-1][0] if i != 0 else None
                        c=new_date_list[i][0]
                        f=new_date_list[i+1][0] if i != len(new_date_list) - 1 else None
                        is_this_good(p, c, f)
        except Exception as e:
            logger.error(e)

    # ! Course per Ped
    def course_per_ped():
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
        # plt.show()

    def course_count():
        text_to_find = '# course'
        new_line=f'# {len(course)}\n'
        with open('data.py', encoding='utf-8', mode='r') as file:
            lines = file.readlines()
        for i in range (0, len(lines)):
            if text_to_find in lines[i]:
                lines.pop(i+1)
                lines.insert(i+1, new_line)
                break
        with open('data.py', encoding='utf-8', mode='w') as file:
            file.writelines(lines)

    def lun_date_convert():
        u_inp=input('Sol to Lu / Lu to Sol / nvm (1, 2, ?)\n')
        os.system('cls')
        day=int(input("Day: "))
        month=int(input("Month: "))
        year=int(input("Year: "))
        print('---')
        if u_inp == '2':
            lu=Lunar(year, month, day)
            sol=Converter.Lunar2Solar(lu)
            print(f'{sol.day}/{sol.month}/{sol.year}')

        elif u_inp=='1':
            sol=Solar(year, month, day)
            lu=Converter.Solar2Lunar(sol)
            print(f'{lu.day}/{lu.month}/{lu.year}')

def cal_pecent(item, total):
    return round(item*100/total, 2)

class hard_function:
    
    def source_summary():
        # is_chart=False if input("Skip Chart? (y=1)\n")=='1' else True
        is_chart=False
        remain=get_total(None)
        total=get_positive_total()
        con_t=get_total('t', True)
        con_e=get_total('e', True)
        con_i=get_total('i')
        con_s=get_total('s')
        con_c=get_crochet_total()
        con_t_p=remains[0][1]

        per_t = cal_pecent(con_t, total)
        per_con_t_p = cal_pecent(con_t_p, total)
        per_e = cal_pecent(con_e, total)
        per_c = cal_pecent(con_c, total)
        per_i = cal_pecent(con_i, total)
        per_s = cal_pecent(con_s, total)
        per_total = sum([per_t, per_con_t_p, per_e, per_c, per_i, per_s])
        
        table = PrettyTable()
        table.field_names = ["Category", "Value", "Percent"]
        table.align["Percent"] = "r"
        table.align["Category"] = "l"
        table.align["Value"] = "r"

        data = [
            {"Category": "QuyDen", "Value": f"{con_t_p:>12,}", "Percent": f"{per_con_t_p:.2f}"},
            {"Category": "DanLen", "Value": f"{con_c:>12,}", "Percent": f"{per_c:.2f}"},
            {"Category": "A", "Value": f"{con_t:>12,}", "Percent": f"{per_t:.2f}"},
            {"Category": "E", "Value": f"{con_e:>12,}", "Percent": f"{per_e:.2f}"},
            {"Category": "Lai", "Value": f"{con_i:>12,}", "Percent": f"{per_i:.2f}"},
            {"Category": "Chi tieu", "Value": f"{con_s:>12,}", "Percent": f"{per_s:.2f}"},
            {"Category": "----------", "Value": "--------------", "Percent": "------------"},
            {"Category": "So du", "Value": f"{remain:>12,}", "Percent": f"{per_total:.2f}"},
        ]
        
        for entry in data:
            table.add_row([entry["Category"], entry["Value"], entry["Percent"]])
            
        print('\n                     *                      \n')
        print(table)
        print(remain)
        
        table.clear_rows()
        print('\n                     *                      \n')
        
        con_t=con_t_p+con_t
        con_e=con_e+con_c
        per_t=round(con_t*100/total, 2)
        per_e = round(con_e*100/total, 2)
        
        table.add_row(["A", f"{con_t:>12,}", f"{per_t:.2f}"])
        table.add_row(["E", f"{con_e:>12,}", f"{per_e:.2f}"])
        table.add_row(["Lai", f"{con_i:>12,}", f"{per_i:.2f}"])
        table.add_row(["Chi tieu", f"{con_s:>12,}", f"{per_s:.2f}"])
        
        table.add_row(["--------", "------------", "----------"])
        table.add_row(["So du", f"{remain:>12,}", f"{per_total:.2f}"])

        print(table)

        if is_chart:
            labels=[f'T', f'E', f'I']

            plt.figure(figure=( 1.3, 1.4))
            plt.pie([
                per_t+per_con_t_p, 
                per_e+per_c, 
                abs(100- per_t-per_con_t_p-per_e-per_c)
                ], labels=labels,explode=[0.05, 0.05, 0.05])
            plt.legend()
            plt.show()
   
    def _history():
        histoies=sorted(remains, key=lambda x: x[0])
        for item in histoies:
            date=item[0].strftime("%d/%m/%y")
            amount=f'{item[1]:,}'
            name=str(item[2]).upper()
            color=Fore.LIGHTGREEN_EX
            if name == 'T':
                color=Fore.LIGHTWHITE_EX
            if name == 'E':
                color=Fore.LIGHTYELLOW_EX
            
            source=name
            # source=col_txt(color, name)+Fore.BLACK
            date=col_txt(color, date)+Fore.BLACK

            print(col_txt(Fore.BLACK, f'({date} - {source}): {amount}'))

    def total_amount_monthly(histories):
        if histories == None:
            histories = remains

        # ! Plotting change monthly
        # Sample data
        data = [sublist[:3] for sublist in histories]
        data.sort(key= lambda x: x[0])

        # Convert data to DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Amount', 'Source'])

        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Extract month from 'Date'
        df['Month'] = df['Date'].dt.to_period('M')
        df['Total Cumulative Sum'] = df.groupby('Month')['Amount'].cumsum()

        # Group data by 'Month' and 'Source', then calculate cumulative sum
        monthly_sum = df.groupby(['Month', 'Source'])['Amount'].sum().groupby(level=1).cumsum()

        # Pivot the table to have 'i', 'e', and 't' as columns
        pivot_table = monthly_sum.reset_index().pivot(index='Month', columns='Source', values='Amount').fillna(0)
        print(pivot_table.shape)

        # Plot stacked column chart
        pivot_table.plot(kind='bar', stacked=True, figsize=(5, 3))
        plt.plot([-1, pivot_table.shape[0]+1] ,[save_goal,save_goal], linestyle='--')
        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Total amount monthly')
        plt.legend(title='Source')
        plt.xticks(rotation=0)
        plt.show()

    def amount_each_month(histories):
        if histories == None:
            histories = remains

        # ! Plotting each month
        # Sample data
        data = [sublist[:3] for sublist in histories if sublist[2] != 'i']
        data.sort(key= lambda x: x[0])

        # Convert data to DataFrame
        df = pd.DataFrame(data, columns=['Date', 'Amount', 'Source'])

        # Convert 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Extract month from 'Date'
        df['Month'] = df['Date'].dt.to_period('M')

        # Group data by 'Month' and 'Source', then calculate the sum for each group
        monthly_sum = df.groupby(['Month', 'Source'])['Amount'].sum()

        # Pivot the table to have 'i', 'e', and 't' as columns
        pivot_table = monthly_sum.unstack(fill_value=0)

        # Plot stacked column chart
        pivot_table.plot(kind='bar', stacked=True, figsize=(5, 3))
        plt.plot([-1, pivot_table.shape[0]+1] ,[save_goal,save_goal], linestyle='--')

        plt.xlabel('Month')
        plt.ylabel('Amount')
        plt.title('Amount each month')
        plt.legend(title='Source')
        plt.xticks(rotation=0)
        plt.show()
    
    def find_anni_date_that_is_first_of_lunar_month():
        # yearFrom = int(input('From Which Year? (number/0)\n'))
        yearLimit = int(input('To Which Year? (number/0)\n'))
        now=datetime.now()
        day_list=[]
        try:
            if (yearLimit >= now.year):
                for year in range(now.year, yearLimit+1):
                # for year in range(yearFrom, yearLimit+1):
                    for month in range(1, 13):
                        solar_day = datetime(day=3, month=month, year=year)
                        lunar_day = sol_to_lu_date(solar_day)
                        if(lunar_day.day==1):
                            lunar_day_format =f'{str(lunar_day.day).zfill(2)}/{str(lunar_day.month).zfill(2)}/{str(lunar_day.year%1000).zfill(2)} '
                            day_list.append(f'{solar_day.strftime("%d/%m/%Y")} -> {col_txt(Fore.BLACK, lunar_day_format)}')
            for day in day_list:
                print(day)
        except Exception as e:
            logger.error(e)
    
    def find_dob_that_lunar_month_is_not_7():
        day=int(input("Day: "))
        month=int(input("Month: "))
        year=int(input("Year: "))
        to_which_year=int(input("To which year: "))
        sol=Solar(year, month, day)
        day_list=[]
        print()
        while (to_which_year!=sol.year):
            lunar_day=Converter.Solar2Lunar(sol)
            if (lunar_day.month == 7 and lunar_day.day == 1):
                solar_day = datetime(sol.year, sol.month, sol.day)
                lunar_str =f'{str(lunar_day.day).zfill(2)}/{str(lunar_day.month).zfill(2)}/{str(lunar_day.year%1000).zfill(2)}'
                day_str =f'{solar_day.strftime("%d/%m/%Y")} ({lunar_str})'
                print(day_str)
                day_list.append(day_str)
            sol=Solar(sol.year+1, month, day)
    
    def time_table():
        subject, current_date = get_current_subject(tkb)
        color = current_day_color =Fore.LIGHTWHITE_EX
        
        table = PrettyTable()
        table.field_names = ["STT", "Day", "From", "To", "Hour", "Room", "Subject Name", "Class Code"]
        tkb_sorted = sorted(tkb, key=lambda x: (x['day'], x['ped_from']))
        first_date=f"T{tkb_sorted[0]['day']}"
        stt=1
        for entry in tkb_sorted:
            p_from = entry['ped_from']
            p_to = entry['ped_to']
            date = f"T{entry['day']}"
            if (date!=first_date):
                table.add_row(['---','---', '----', '--', '-----', '-------', '-----------------------------------------------------------------------', '------------'])
                first_date=date
            if (entry['day']== current_date):
                current_day_color=Fore.LIGHTGREEN_EX
            if (entry['name']== subject):
                color=Fore.LIGHTGREEN_EX
            table.add_row([stt, col_txt(current_day_color, date), p_from, p_to , col_txt(color, period_to_hour(p_from, p_to)), col_txt(color, entry['room']), col_txt(color, entry['name']), entry['class_code']])
            stt+=1
            color=current_day_color=Fore.LIGHTWHITE_EX
            
        table.align = "l"
        table.align["STT"] = "c"

        print(table)
        
        is_continue=True
        while is_continue:
            chosing=(input('STT: (?/) '))
            if chosing=='':
                break
            chosing=int(chosing)
            find_subject(chosing, tkb_sorted)
        
def period_to_hour(p_from, p_to):
    return f"{period[p_from][0]}-{period[p_to][-1]}"

def get_current_subject(tkb):
    now = datetime.now()
    current_day = now.isoweekday() + 1
    current_hour = int(now.strftime('%H'))

    for entry in tkb:
        hour_from = period[entry['ped_from']][0]
        hour_to = period[entry['ped_to']][-1]
        if entry['day'] == current_day and hour_from <= current_hour <= hour_to:
            return entry['name'], entry['day']
        if entry['day'] == current_day:
            return '', current_day
    return '', 0

def find_subject(id, tkb_sort):
    info= tkb_sort[id-1]
    name=info['name']
    class_code=info['class_code']
    value=info['value']
    print(f"[{class_code}]: {name} - {value} tín.\n")