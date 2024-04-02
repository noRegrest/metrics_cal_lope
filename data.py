from datetime import datetime

b=4000
gift=500
save=500
gas=500
per=500
elses=2000
class im_date:
    first_date=datetime(day=3, month=11, year=2023)
    
    val=datetime(day=18, month=2, year=2024)
    e_BD=datetime(day=20, month=8, year=2004)
    t_BD=datetime(day=14, month=5, year=2000)
    
    mama_e_BD=datetime(day=11, month=3, year=1975)
    
# commitment, sharing, lope
t_data=[
  [[9.5, 9.0, 9.5], datetime(day=6, month=1, year=2024)],
  [[8.5, 6.5, 7.0], datetime(day=27, month=1, year=2024)],
  [[7.5, 6.0, 6.0], datetime(day=29, month=1, year=2024)],
  [[7.0, 6.0, 6.0], datetime(day=30, month=1, year=2024)],
  [[8.0, 7.5, 7.0], datetime(day=1, month=2, year=2024)],
  [[7.5, 7.0, 6.5], datetime(day=2, month=2, year=2024)],
  [[8.0, 7.5, 7.5], datetime(day=4, month=2, year=2024)],
  [[8.5, 7.5, 8.5], datetime(day=5, month=2, year=2024)],
  [[8.5, 8.0, 9.0], datetime(day=7, month=2, year=2024)],
  [[9.0, 8.5, 9.5], datetime(day=10, month=2, year=2024)],
  [[9.5, 9.0, 10.0], datetime(day=14, month=2, year=2024)],
  [[10.0, 9.0, 10.0], datetime(day=18, month=2, year=2024)],
  [[10.0, 9.5, 9.5], datetime(day=20, month=2, year=2024)],
  [[9.5, 9.0, 9.5], datetime(day=29, month=2, year=2024)],
  [[10.0, 10.0, 10.0], datetime(day=3, month=3, year=2024)],
  [[9.5, 9.5, 9.0], datetime(day=18, month=3, year=2024)],
  [[9.0, 8.5, 9.0], datetime(day=19, month=3, year=2024)],
  [[9.0, 5.0, 8.5], datetime(day=23, month=3, year=2024)],
  [[10.0, 9.0, 9.5], datetime(day=24, month=3, year=2024)],
]
# t data

e_data=[
  [[8.0, 8.5, 8.0], datetime(day=6, month=1, year=2024)],
  [[6.0, 7.0, 6.0], datetime(day=27, month=1, year=2024)],
  [[7.0, 6.5, 6.0], datetime(day=29, month=1, year=2024)],
  [[7.0, 6.5, 6.5], datetime(day=30, month=1, year=2024)],
  [[7.5, 7.5, 7.5], datetime(day=1, month=2, year=2024)],
  [[6.0, 6.0, 5.0], datetime(day=2, month=2, year=2024)],
  [[7.0, 7.5, 8.0], datetime(day=4, month=2, year=2024)],
  [[8.0, 7.5, 8.5], datetime(day=5, month=2, year=2024)],
  [[8.0, 8.0, 9.0], datetime(day=7, month=2, year=2024)],
  [[9.0, 8.5, 9.5], datetime(day=10, month=2, year=2024)],
  [[9.5, 9.0, 9.5], datetime(day=14, month=2, year=2024)],
  [[10.0, 10.0, 10.0], datetime(day=18, month=2, year=2024)],
  [[10.0, 10.0, 10.0], datetime(day=20, month=2, year=2024)],
  [[10.0, 9.0, 9.5], datetime(day=29, month=2, year=2024)],
  [[10.0, 10.0, 10.0], datetime(day=3, month=3, year=2024)],
  [[10.0, 9.5, 10.0], datetime(day=18, month=3, year=2024)],
  [[9.5, 9.5, 9.0], datetime(day=19, month=3, year=2024)],
  [[8.0, 9.5, 8.5], datetime(day=23, month=3, year=2024)],
  [[10.0, 9.5, 10.0], datetime(day=24, month=3, year=2024)],
]
# e data

# t0 is initial data
# t1 is before 
# t2 is aright after (29/01/24)
# t3 is after 1 d
# t[-1] is today 

ped=[
  datetime(day=20, month=10, year=2023),
  datetime(day=24, month=11, year=2023),
  datetime(day=18, month=12, year=2023),
  datetime(day=14, month=1, year=2024),
  datetime(day=14, month=2, year=2024),
  datetime(day=17, month=3, year=2024),
]
# ped

course=[
  datetime(day=16, month=12, year=2023),
  datetime(day=27, month=12, year=2023),
  datetime(day=29, month=12, year=2023),
  datetime(day=1, month=1, year=2024),
  datetime(day=5, month=2, year=2024),
  datetime(day=18, month=2, year=2024),
  datetime(day=19, month=2, year=2024),
  datetime(day=24, month=2, year=2024),
  datetime(day=25, month=2, year=2024),
  datetime(day=1, month=3, year=2024),
  datetime(day=7, month=3, year=2024),
  datetime(day=10, month=3, year=2024),
  datetime(day=12, month=3, year=2024),
  datetime(day=16, month=3, year=2024),
  datetime(day=24, month=3, year=2024),
  datetime(day=29, month=3, year=2024),
]
# course
# 16

pred_ped=datetime(day=15, month=4, year=2024)
# pred

# date | quantity | 't' or 'e' or 'i'
remains=[
  [datetime(day=18, month=3, year=2024), 2501087, 't'],
  [datetime(day=19, month=3, year=2024), 520804, 't'],
  [datetime(day=19, month=3, year=2024), 200000, 'e'],
  [datetime(day=20, month=3, year=2024), 274, 'i'],
  [datetime(day=21, month=3, year=2024), 352, 'i'],
  [datetime(day=22, month=3, year=2024), 352, 'i'],
  [datetime(day=23, month=3, year=2024), 352, 'i'],
  [datetime(day=24, month=3, year=2024), 352, 'i'],
  [datetime(day=25, month=3, year=2024), 352, 'i'],
  [datetime(day=26, month=3, year=2024), 352, 'i'],
  [datetime(day=27, month=3, year=2024), 352, 'i'],
  [datetime(day=28, month=3, year=2024), 352, 'i'],
  [datetime(day=29, month=3, year=2024), 353, 'i'],
  [datetime(day=29, month=3, year=2024), 30000, 'e'],
  [datetime(day=30, month=3, year=2024), 353, 'i'],
  [datetime(day=31, month=3, year=2024), 353, 'i'],
  [datetime(day=31, month=3, year=2024), 50000, 'e'],
  [datetime(day=1, month=4, year=2024), 353, 'i'],
  [datetime(day=1, month=4, year=2024), 50000, 'e'],
  [datetime(day=2, month=4, year=2024), 362, 'i'],
  # [datetime(day=24, month=3, year=2024), 30000, 'e'],

]
