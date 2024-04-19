from data import history
import pandas as pd

is_e=True if input('E? (1/?)') == '1' else False
is_save=True if input('Save? (1/?)') == '1' else False

if is_e:
    defined_columns=['how much', 'who', 'what for', 'how many people']
    each_one='each one'
else:
    defined_columns=['Thành tiền', 'Người chi', 'Danh mục', 'Nhóm người']
    each_one='Chia đầu người'

how_much=defined_columns[0]
who=defined_columns[1]
what_for=defined_columns[2]       
how_many_p=defined_columns[3]

df = pd.DataFrame(history, columns=defined_columns)

# ! History
column_to_move = df.pop(what_for)
df = pd.concat([column_to_move, df], axis=1)
df=df.sort_values([who, how_much])
df.reset_index(drop=True, inplace=True)

# ! Summary
# grouped_df=df.groupby(how_many_p)
grouped_df=df.groupby(who)
total_by_people_group=grouped_df[how_much].sum()
by_who = grouped_df[who].max()
summary_df = pd.DataFrame({who: by_who.values, how_much: total_by_people_group.values, how_many_p: total_by_people_group.index})
# summary_df[each_one]=summary_df[how_much]/summary_df[how_many_p]

print(df)
print('-----')
print(summary_df)  

if is_save:
    with pd.ExcelWriter('thuchi.xlsx', engine='xlsxwriter', engine_kwargs={'options': {'encoding': 'utf-8'}}) as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=who)
        summary_df.to_excel(writer, sheet_name='Sheet2', index=how_many_p)