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
    print(col_txt(Fore.BLACK,'-----\n')+f'{course_date_format}:')

    if previous_ped is not None:
        dif=(course_date-previous_ped).days+1
        color = Fore.LIGHTGREEN_EX if dif >= 20 else Fore.LIGHTRED_EX
        ped_date_format=previous_ped.strftime("%d/%m/%y")
        print(col_txt(Fore.LIGHTBLACK_EX, ' (p) ') + col_txt(color, f'{ped_date_format}: ({dif})'))

    if follow_ped is not None:
        dif=(follow_ped-course_date).days
        color = Fore.LIGHTGREEN_EX if dif <10 else Fore.LIGHTRED_EX
        ped_date_format=follow_ped.strftime("%d/%m/%y")
        print(col_txt(Fore.LIGHTBLACK_EX, ' (f) ') + col_txt(color, f'{ped_date_format}: ({dif})'))
        
class export_function:
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
            print(e)

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
            last_color = Fore.GREEN if (last_for%100 ==0 or last_for%100==99 or last_for%100==98) else Fore.RESET

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

            print('Been for:'+col_txt(last_color,f' {last_for}')+' days')
            
            if last_for_rel.years>0:
                text=f'{last_for_rel.years} years, {last_for_rel.months} months, {last_for_rel.days} days'
            else:
                text=f'{last_for_rel.months} months, {last_for_rel.days} days'

            print(col_txt(Fore.BLACK, text))
            print('')
            print(f'Till e {e_y+1} BD: {is_near_e_BD} days ({round(to_e_BD/30, 1)})')
            print(f'Till t {t_y+1} BD: {is_near_t_BD} days ({round(to_t_BD/30, 1)})')
            # dif = relativedelta(im_date.e_BD,im_date.t_BD)
            # print(col_txt(Fore.BLACK, f'Dif: {dif.years} years, {dif.months} months, {dif.days} days'))
        except Exception as e:
            print(e)

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

            distances = [(date_list[i+1] - date_list[i]).days for i in range(len(date_list) - 1)]
            mean=round(s.mean(distances), 2)
            print(f'Circle: {mean} days ' + col_txt(Fore.BLACK, f'{distances}'))

            predict=date_list[-1]+timedelta(days=mean)
            pred_distance=(predict-today).days
            if pred_distance<=0:
                print(f'Has it happen? '+col_txt(Fore.LIGHTYELLOW_EX, f'({predict.strftime("%d/%m/%Y")})')+ col_txt(Fore.BLACK, f' ({-pred_distance} days ago)'))
            else:
                print(f'Next circle starts at: '+col_txt(Fore.LIGHTYELLOW_EX,f'{predict.strftime("%d/%m/%Y")}')+f' (in {pred_distance})')

            text_to_find='# pred'
            new_line=f'pred_ped=datetime(day={predict.day}, month={predict.month}, year={predict.year})\n'

            with open('data.py', 'r') as file:
                lines = file.readlines()
            for i in range (0, len(lines)):
                if text_to_find in lines[i]:
                    lines.pop(i-1)
                    lines.insert(i-1, new_line)
                    break
            with open('data.py', 'w') as file:
                file.writelines(lines)

        except Exception as e:
            print(e)

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
                with open('data.py', 'r') as file:
                    lines = file.readlines()
                for i in range (0, len(lines)):
                    if text_to_find in lines[i]:
                        lines.insert(i-1, new_line)
                        break
                with open('data.py', 'w') as file:
                    file.writelines(lines)
                print(col_txt(Fore.GREEN,'Done'))
            else:
                print(col_txt(Fore.GREEN, 'Stopped'))

        except Exception as e:
            print(e)

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
                    x_date=datetime.now()
                    x=[ped[-1], pred_ped]
                    y=[3, 4]
                    y_date = y[0] + (y[1] - y[0]) * ((x_date - x[0]).days / (x[1] - x[0]).days)
 
                    plt.figure(figsize=(5, 3))
                    plt.plot([x_date], [y_date], color='red', label='Today', marker='X' )
                    plt.plot(ped_date[-3:], range(1, 3+1), label='Ped', marker='o')
                    plt.plot([ped_date[-1], pred_ped], [3, 4], label='Predict Ped', marker='*', linestyle='--')

                    # plt.plot([ped_date[-1]], [0], label='Ped', marker='o')
                    # plt.plot([ped_date[-1], pred_ped], [0, 0], label='Predict Ped', marker='*', linestyle='--')
                    # plt.plot([x_date], [0], color='red', label='Today', marker='X' )

                    plt.xlabel('Date')
                    plt.ylabel('Index')
                    plt.grid(True)
                    plt.xticks(rotation=45)
                    plt.title('2. Ped Plot')

                elif chosing == '3':
                    plt.figure(figsize=(5, 3))
                    plt.plot(cours_date, range(1, len(cours_date)+1), label='Course', marker='o')
                    plt.plot(ped_date, range(1, len(ped_date)+1), label='Ped', marker='o')
                    plt.plot([datetime.now(), datetime.now()], [0, 10], label='Current Date', marker='X', linestyle='-.')
                    plt.plot([im_date.first_date, im_date.first_date], [0, 10], label='First', marker='D', color='purple', linestyle='-.')

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
            print(e)

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
            print(e)

