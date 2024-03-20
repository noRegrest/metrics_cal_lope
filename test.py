import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data import im_date, ped, course, t_data, e_data, pred_ped

def find_y(x1, x2, y1, y2, given_x):
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return m * given_x + b     

def find_y_by_time(x1: datetime, x2: datetime, y1, y2, given_x: datetime):
    return find_y(x1.timestamp(), x2.timestamp(), y1, y2, given_x.timestamp())

skip_number=int(input('? nearest months\n'))

if skip_number==0:
    skip_number=len(ped)

ped_date= ped[-skip_number:]
course_date = [dates for dates in course if dates >= ped_date[0]]

x_now = datetime.now()
y_now = find_y_by_time(ped[-1], pred_ped, len(ped_date)-1, len(ped_date), x_now)

x_safe_day = pred_ped - timedelta(days=10)
y_safe_day = find_y_by_time(ped_date[-1], pred_ped, len(ped_date)-1, len(ped_date), x_safe_day)

plt.figure(figsize=(5, 3))
plt.plot([ped_date[-1], pred_ped], [len(ped_date)-1, len(ped_date)], label='Predict Ped', marker='o', linestyle='--', color=('#6E6E6E'))
plt.plot(ped_date, range(0, len(ped_date)), label='Ped', marker='o', color=('#6E6E6E'))
plt.plot(x_safe_day, y_safe_day, 'go')
plt.plot([x_now], [y_now], label='Today', marker='d', color='#1F77B4' )

# ! course
for  j in range(0, len(course_date)):
    course_new=[[course_date[j], 1]]
    ped_new=[[item, 0] for item in ped]
    new_date_list = ped_new + course_new
    new_date_list.sort(key=lambda x: x[0])

    for i in range(0, len(new_date_list)):
        if new_date_list[i][-1] == 1:
            x1=new_date_list[i-1][0] if i != 0 else None
            x_given=new_date_list[i][0]
            x2=new_date_list[i+1][0] if i != len(new_date_list) - 1 else None

            y1=ped_date.index(x1)

            if x2 == None:
                x2 = pred_ped
                y2 = skip_number+1
            else:
                y2=ped_date.index(x2)
            
            y_to_find=find_y_by_time(x1, x2, y1, y2, x_given)
            color = 'green' if (x2-x_given).days<=10 else 'red'
            marker = 'v' # if (x2-x_given).days<=10 else 'd'
            plt.plot(x_given, y_to_find, marker=marker, color=color)

plt.xlabel('Date')
plt.ylabel('Index')
plt.grid(True)
plt.xticks(rotation=45)
plt.title('P/C')

plt.legend()
plt.tight_layout()
plt.show()
print('')