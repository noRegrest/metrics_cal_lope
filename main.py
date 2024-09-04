import os
from colorama import Fore
from services.consonant import toNH
from services.lunar import luanr
from utils import col_txt
from services.function import soft_function as f, hard_function as hf

is_continue=True

while is_continue:
    os.system('cls')

    chosen = (input(col_txt(
        Fore.BLACK,'Choose one, anything else to stop\n')
                    + '1. Counting ds'
                    + '\n2. Circle'
                    + '\n3. Safety'
                    + '\n4. Plotting stuffs'
                    + '\n5. Change percent calcu'
                    + '\n6. Insert'
                    + '\n7. Course/Ped'
                    + '\n8. Calendar'
                    + '\n9. Remains'
                    + '\n10. Vegetable days'
                    + '\n11. Lunar year'
                    + '\n12. Nhờn'
                    + '\n13. FindFirstBoD'
                    + Fore.BLACK
                    + '\n=========\n'
                    + Fore.RESET))
    
    print(col_txt(Fore.BLACK, '\n=========\n'))
    os.system('cls')
    print()

    # ? Counting
    if chosen == '1':
        f.cal_date()

    # ? Circle
    elif chosen == '2':
        f.pred_pe()

    # ? Evaluate course safety
    elif chosen == '3':
        f.evaluate_safety()

    # ? Plotting course
    elif chosen == '4':
        f.plot_stuffs()

    # ? Change percent calcu
    elif chosen == '5':
        is_predict=False
        # is_skip_plot = False if input("Skip plotting? (yes= 1)\n")=='1' else  True
        is_skip_plot=False
        print(col_txt(Fore.BLACK, '\n=========\n'))
        f.change_percent_cal('T data', is_plot=is_skip_plot)

        print(col_txt(Fore.BLACK, '\n=========\n'))
        f.change_percent_cal('E data', is_plot=is_skip_plot)

    # ? Insert new thing
    elif chosen == '6':
        input_user = input("Course/Ped/T data/E data?\n (1/2/3/4/0)\n")
        if input_user == '1':
            f.insert_date('course')
        if input_user == '2':
            f.insert_date('ped')
        if input_user == '3':
            f.insert_date('t data')
        if input_user == '4':
            f.insert_date('e data')
    
    # ? Course per Ped
    elif chosen == '7':
        f.course_per_ped()

    # ? Calendar
    elif chosen == '8':
        f.lun_date_convert()

    # ? Remains
    elif chosen == '9':
        hf.source_summary()

    # ? Vegetable days
    elif chosen == '10':
        hf.find_anni_date_that_is_first_of_lunar_month()

    # ? Lunar year
    elif chosen == '11':
        luanr()

    # ? to NH
    elif chosen == '12':
        toNH()

    # ? to NH
    elif chosen == '13':
        hf.find_dob_that_lunar_month_is_not_7()
 
    # ? test
    elif chosen == '111':
        hf.time_table()
        
    # ? Stop
    else:
        is_continue=False
        continue

    print(col_txt(Fore.BLACK, '\n=========\n'))

    is_continue=True if input('Menu? (yes= 1)\n')=='1' else False

os.system('cls')
f.course_count()
