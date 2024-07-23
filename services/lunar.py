
# Define dictionaries for lunar years and animals
import os

from colorama import Fore

from utils import col_txt

# Define lunar years in SCN and TCN orders
lunarSCN = [
    {"name": "Canh", "value": 0},
    {"name": "Tân", "value": 1},
    {"name": "Nhâm", "value": 2},
    {"name": "Quý", "value": 3},
    {"name": "Giáp", "value": 4},
    {"name": "Ất", "value": 5},
    {"name": "Bính", "value": 6},
    {"name": "Đinh", "value": 7},
    {"name": "Mậu", "value": 8},
    {"name": "Kỉ", "value": 9}
]

lunarTCN = [
    {"name": "Canh", "value": 1},
    {"name": "Tân", "value": 0},
    {"name": "Nhâm", "value": 9},
    {"name": "Quý", "value": 8},
    {"name": "Giáp", "value": 7},
    {"name": "Ất", "value": 6},
    {"name": "Bính", "value": 5},
    {"name": "Đinh", "value": 4},
    {"name": "Mậu", "value": 3},
    {"name": "Kỉ", "value": 2},
]

# Define lunar animals
lunar_animals = [
    {"name": "Tí", "value": 0},
    {"name": "Sửu", "value": 1},
    {"name": "Dần", "value": 2},
    {"name": "Mão", "value": 3},
    {"name": "Thìn", "value": 4},
    {"name": "Tị", "value": 5},
    {"name": "Ngọ", "value": 6},
    {"name": "Mùi", "value": 7},
    {"name": "Thân", "value": 8},
    {"name": "Dậu", "value": 9},
    {"name": "Tuất", "value": 10},
    {"name": "Hợi", "value": 11},
]

def find_lunar_positive(year):
    lunarValue = abs(year % 10)
    diff = abs(year - 1960)
    animalNumber = diff % 12

    if year < 1960:
        if animalNumber != 0:
            animalNumber = 12 - animalNumber
    
    start = next(item["name"] for item in lunarSCN if item["value"] == lunarValue)
    end = next(item["name"] for item in lunar_animals if item["value"] == animalNumber)
    return f"{start} {end}"

def find_lunar_negative(year):
    yearP = abs(year)
    lunarValue = yearP % 10
    animalNumber = 9 - yearP % 12

    if animalNumber < 0:
        animalNumber += 12
    
    start = next(item["name"] for item in lunarTCN if item["value"] == lunarValue)
    end = next(item["name"] for item in lunar_animals if item["value"] == animalNumber)
    return f"{start} {end}"

def find_lunar_by_year(year):
    if year >= 0:
        return find_lunar_positive(year)
    else:
        return find_lunar_negative(year)

def find_lunar_by_years(from_year, to_year):
    arr = []
    for i in range(from_year, to_year + 1):
        arr.append(find_lunar_by_year(i))
    return arr

def find_year_by_lunar(lunar_to_search, from_year=1800, to_year=2024):
    years = []
    lunar_lower = lunar_to_search.lower()
    for i in range(from_year, to_year + 1):
        result = find_lunar_by_year(i).lower()
        if lunar_lower in result:
            years.append(i)
    return {"search": lunar_to_search, "years": years}

def luanr():
    is_continue=True

    while is_continue:
        try:  
            chosing=input('Year to Lunar or Find year by Lunar ( 1 / 2 / anything else )\n')
            os.system('cls')
            if (chosing == '1'):
                year = int(input('Input year: '))
                print('=> '+find_lunar_by_year(year)) 

            elif (chosing == '2'):
                yearFrom = int(input('From which year? '))
                yearTo = int(input('To which year? '))
                search = input('What to find?')
                result = find_year_by_lunar(search, yearFrom, yearTo)['years']
                if search == '':
                    for year in result:
                        print(f'{year}' + ': ' +find_lunar_by_year(year)) 
                else:
                    print(f'=> {result}') 

            else:
                is_continue=False
                continue

            is_continue=True if input('\n---\nContinue? (yes= 1)\n')=='1' else False
            os.system('cls')
        except Exception as e:
            print(col_txt(fore=Fore.RED,text =  f'{e}'))