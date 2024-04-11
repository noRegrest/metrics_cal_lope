from data import history
import pandas as pd

is_e=True if input('E? (1/?)') == '1' else False
is_save=True if input('Save? (1/?)') == '1' else False

if is_e:
    defined_columns=['how much', 'who', 'what for', 'how many people']
else:
    defined_columns=['Thành tiền', 'Người chi', 'Danh mục', 'Nhóm người']

how_much=defined_columns[0]
who=defined_columns[1]
what_for=defined_columns[2]       
how_many_p=defined_columns[3]

df = pd.DataFrame(history, columns=defined_columns)
df=df.sort_values([who, how_much])
print(df)
if is_save:
    df.to_csv('summary/history.csv', index=who)

print('-----')

grouped_df=df.groupby(how_many_p)
total_by_people_group=grouped_df[how_much].sum()
by_who = grouped_df[who].max()

summary_df = pd.DataFrame({how_much: total_by_people_group.values, who: by_who.values}, index=total_by_people_group.index)

print(summary_df)  
if is_save:
    summary_df.to_csv('summary/summary.csv', index=how_many_p)