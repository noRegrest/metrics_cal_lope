import os
import math
import numpy as np
import statistics as s
import matplotlib.pyplot as plt

from colorama import Fore
from utils import col_txt
from datetime import datetime, timedelta
from data import remains

class cal_function():

    def total():
        return sum([m[1] for m in remains])
    
    def condition_total(source = 't'or 'e' or 'i'):
        return sum([m[1] for m in remains if m[2] == source ])
    
    def source_summary():
        total=cal_function.total()
        con_t=cal_function.condition_total('t')
        con_e=cal_function.condition_total('e')
        con_i=cal_function.condition_total('i')

        per_t = round(con_t*100/total, 2)
        per_e = round(con_e*100/total, 2)
        per_i = round(con_i*100/total, 2)

        print(f'===\nTotal: \t{total:>12,}')
        print(Fore.BLACK+f'T: \t{con_t:>12,} ({per_t}%)')
        print(f'E: \t{con_e:>12,} ({per_e}%)')
        print(f'I: \t{con_i:>12,} ({per_i}%)'+Fore.RESET)

    def pie_chart():
        print('coming soon')
    
    def history():
        # t_history=[t for t in remains if t[2] == 't']
        # e_history=[t for t in remains if t[2] == 'e']
        # i_history=[t for t in remains if t[2] == 'i']

        # plt.figure(figsize=(5, 3))
        # plt.plot([t[0] for t in t_history], [t[1] for t in t_history])
        # plt.plot([t[0] for t in e_history], [t[1] for t in e_history])
        # plt.plot([t[0] for t in i_history], [t[1] for t in i_history])
        # plt.grid(axis='y', linestyle='--', alpha=0.7, which= 'both')

        time_periods = [t[0] for t in remains]
        values = [t[1] for t in remains]
        processed_values = [sum(values[:i+1]) for i in range(len(values))]

        plt.figure(figsize=(5, 3))

        # Plotting the cumulative growth over time
        plt.plot(time_periods, processed_values, marker='o', linestyle='-')

        # Filling the area below the line with a color
        plt.fill_between(time_periods, processed_values, color='skyblue', alpha=0.4)

        plt.xlabel('Date')
        plt.ylabel('Index')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.show()

cal_function.source_summary()