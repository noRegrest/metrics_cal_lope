from datetime import datetime

b=4000

gift=500
save=500
gas=500
per=500

elses=2000

save_goal = 10e6

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
  [[9.5, 8.5, 8.5], datetime(day=4, month=4, year=2024)],
  [[9.5, 9.0, 8.5], datetime(day=5, month=4, year=2024)],
  [[9.5, 9.5, 9.0], datetime(day=8, month=4, year=2024)],
  [[9.0, 8.5, 8.5], datetime(day=19, month=4, year=2024)],
  [[9.0, 8.5, 9.0], datetime(day=21, month=4, year=2024)],
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
  [[7.0, 8.0, 8.5], datetime(day=4, month=4, year=2024)],
  [[8.0, 8.5, 8.5], datetime(day=5, month=4, year=2024)],
  [[9.5, 9.0, 9.5], datetime(day=8, month=4, year=2024)],
  [[8.5, 8.5, 8.0], datetime(day=19, month=4, year=2024)],
  [[9.0, 9.0, 8.5], datetime(day=21, month=4, year=2024)],
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
  datetime(day=3, month=5, year=2024),
  datetime(day=4, month=6, year=2024),
  datetime(day=8, month=7, year=2024),
  datetime(day=18, month=8, year=2024),
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
  datetime(day=6, month=4, year=2024),
  datetime(day=7, month=4, year=2024),
  datetime(day=9, month=4, year=2024),
  datetime(day=20, month=4, year=2024),
  datetime(day=20, month=6, year=2024),
  datetime(day=25, month=6, year=2024),
  datetime(day=27, month=6, year=2024),
  datetime(day=7, month=7, year=2024),
  datetime(day=24, month=7, year=2024),
  datetime(day=1, month=9, year=2024),
]
# course
# 26

pred_ped=datetime(day=20, month=9, year=2024)
# pred

# date | amount | from_who | source
# source: 
#   - p: personal
#   - m: monthly
#   - s: spending - reason

remains=[
  [datetime(day=18, month=3, year=2024), 2501087, 't', 'p'],

  [datetime(day=19, month=3, year=2024),  520804, 't', 'm'],
  [datetime(day=19, month=3, year=2024),  200000, 'e', 'm'],

  [datetime(day=29, month=3, year=2024),   30000, 'e', 'p'],
  [datetime(day=31, month=3, year=2024),   50000, 'e', 'p'],
  [datetime(day= 1, month=4, year=2024),   50000, 'e', 'p'],

  [datetime(day= 3, month=4, year=2024),  200000, 'e', 'm'],
  [datetime(day= 8, month=4, year=2024),  501000, 't', 'm'],

  [datetime(day= 6, month=5, year=2024),  500000, 't', 'm'],
  [datetime(day= 6, month=5, year=2024),  500000, 'e', 'm'],

  [datetime(day= 5, month=6, year=2024),  500000, 't', 'm'],
  [datetime(day= 5, month=6, year=2024),  500000, 'e', 'm'],
 
  [datetime(day= 8, month=7, year=2024),  500000, 't', 'm'],
  [datetime(day= 8, month=7, year=2024),  500000, 'e', 'm'],
 
  [datetime(day= 8, month=8, year=2024),  500000, 't', 'm'],
  [datetime(day= 8, month=8, year=2024),  500000, 'e', 'm'],
 
  [datetime(day=27, month=8, year=2024),  500000, 't', 'm'],
  [datetime(day=27, month=8, year=2024),  500000, 'e', 'm'],
# Hạ long 31-2/9
  [datetime(day=27, month=8, year=2024),-5000000, 's', 'travel'],
 
  [datetime(day= 4, month=9, year=2024),  500000, 't', 'm'],
  [datetime(day= 4, month=9, year=2024),  500000, 'e', 'm'],
  
  [datetime(day=27, month=8, year=2024),  122293, 'i', ' '],

]

# TKB
tkb = [
    {'day': 3, 'ped_from': 7 , 'ped_to': 9,  'room': '304C0',   'class_code': 'INT2204 3',      'value': 3, 'subject_code': 'INT2204', 'name': 'Lập trình hướng đối tượng'},
    {'day': 8, 'ped_from': 3 , 'ped_to': 4,  'room': 'Online1', 'class_code': 'THL1057 2',      'value': 2, 'subject_code': 'THL1057', 'name': 'Nhà nước và pháp luật đại cương'},
    {'day': 4, 'ped_from': 4 , 'ped_to': 6,  'room': 'PH02-C6', 'class_code': 'EAM4005',        'value': 3, 'subject_code': 'EAM4005', 'name': 'Nhập môn thiết kế điều tra khảo sát'},
    {'day': 3, 'ped_from': 4 , 'ped_to': 6,  'room': '304C0',   'class_code': 'INT3110 3',      'value': 3, 'subject_code': 'INT3110', 'name': 'Phân tích và thiết kế hướng đối tượng'},
    {'day': 2, 'ped_from': 7 , 'ped_to': 10, 'room': '212 HT2', 'class_code': 'EDT4005 2',      'value': 3, 'subject_code': 'EDT4005', 'name': 'Phát triển chương trình đào tạo số'},
    {'day': 2, 'ped_from': 2 , 'ped_to': 5,  'room': '213 HT2', 'class_code': 'EDT4008 2',      'value': 3, 'subject_code': 'EDT4008', 'name': 'Phát triển học liệu số'},
    {'day': 6, 'ped_from': 4 , 'ped_to': 6,  'room': 'Online1', 'class_code': 'FLF1107 HP 8',   'value': 5, 'subject_code': 'FLF1107', 'name': 'Tiếng Anh B1'},
    {'day': 3, 'ped_from': 10, 'ped_to': 12, 'room': '303C0',   'class_code': 'EDT4010 2',      'value': 3, 'subject_code': 'EDT4010', 'name': 'Ứng dụng và phát triển công nghệ thông minh (VR, AR, MR) trong giáo dục'}
]


# Period to time
period={
  1: [7, 8],
  2: [8, 9],
  3: [9, 10],
  4: [10, 11],
  5: [11, 12],
  6: [12, 13],
  7: [13, 14],
  8: [14, 15],
  9: [15, 16],
  10: [16, 17],
  11: [17, 18],
  12: [18, 19],
}
 
 
 
 
 
# how much, who, what for, how many people
history=[
    [85, 'Bình', 'rau củ', 7],
    [60, 'Vỹ', 'tim', 7],
    [120, 'Bình', 'tôm', 7],
    [30, 'Vỹ', 'rau', 7],
    [80, 'Vỹ', 'xương', 7],
    [120, 'Bình', 'kim chi, gia vị, thả lẩu', 7],
    [54, 'Bình', 'thịt lợn', 7],
    [260, 'Vỹ', 'thịt vịt', 7],
    [151, 'Trang', 'bi a', 6],
    [130, 'Đạt', 'bi a', 4],
    # [102, 'Vỹ', 'kem, nước ngọt, đá', 7],
    [42, 'Vỹ', 'kem, nước ngọt, đá', 7],
    [155, 'Khương', 'bún trưa', 5],
]

_history=[
    [85, 'Vỹ', 'rau củ', 7],
    [60, 'Vỹ', 'tim', 7],
    [120, 'Vỹ', 'tôm', 7],
    [30, 'Vỹ', 'rau', 7],
    [80, 'Vỹ', 'xương', 7],
    [120, 'Vỹ', 'kim chi, gia vị, thả lẩu', 7],
    [54, 'Vỹ', 'thịt lợn', 7],
    [260, 'Vỹ', 'thịt vịt', 7],
    [151, 'Trang', 'bi a', 6],
    [130, 'Đạt', 'bi a', 4],
    # [102, 'Vỹ', 'kem, nước ngọt, đá', 7],
    [42, 'Vỹ', 'kem, nước ngọt, đá', 7],
    [155, 'Khương', 'bún trưa', 5],
]