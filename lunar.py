
# Define dictionaries for lunar years and animals
import os


lunar = {
    "canh": "Canh ",
    "tan": "Tân ",
    "nham": "Nhâm ",
    "quy": "Quý ",
    "giap": "Giáp ",
    "at": "Ất ",
    "binh": "Bính ",
    "dinh": "Đinh ",
    "mau": "Mậu ",
    "ki": "Kỉ ",
}

animals = {
    "tis": "Tí",
    "suu": "Sửu",
    "dan": "Dần",
    "mao": "Mão",
    "thin": "Thìn",
    "tij": "Tị",
    "ngo": "Ngọ",
    "mui": "Mùi",
    "than": "Thân",
    "dau": "Dậu",
    "tuat": "Tuất",
    "hoi": "Hợi",
}

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
    {"name": animals["tis"], "value": 0},
    {"name": animals["suu"], "value": 1},
    {"name": animals["dan"], "value": 2},
    {"name": animals["mao"], "value": 3},
    {"name": animals["thin"], "value": 4},
    {"name": animals["tij"], "value": 5},
    {"name": animals["ngo"], "value": 6},
    {"name": animals["mui"], "value": 7},
    {"name": animals["than"], "value": 8},
    {"name": animals["dau"], "value": 9},
    {"name": animals["tuat"], "value": 10},
    {"name": animals["hoi"], "value": 11},
]

def find_lunar_positive(year):
    lunarValue = abs(year % 10)
    lunarName = next(item["name"] for item in lunarSCN if item["value"] == lunarValue)
    
    diff = abs(year - 1960)
    animalNumber = diff % 12
    if year < 1960:
        if animalNumber != 0:
            animalNumber = 12 - animalNumber
    
    end = next(item["name"] for item in lunar_animals if item["value"] == animalNumber)
    return f"{lunarName} {end}"

def find_lunar_negative(year):
    yearP = abs(year)
    lunarValue = yearP % 10
    start = next(item["name"] for item in lunarTCN if item["value"] == lunarValue)
    
    animalNumber = 9 - yearP % 12
    if animalNumber < 0:
        animalNumber += 12
    
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

# Testing the functions
# year= int(input('Year: '))
# os.system('cls')

# print(find_lunar_by_year(year))
# Uncomment below lines to test other functions
# print(find_lunar_by_years(1950, 2024))
# print(find_year_by_lunar(lunar["quy"] + animals["mui"]))

def luanr():
    is_continue=True

    while is_continue:
        chosing=input('Year to Lunar or Find year by Lunar ( 1 / 2 / anything else )\n')
        os.system('cls')
        if (chosing == '1'):
            year = int(input('Input year: '))
            print('=> '+find_lunar_by_year(year)) 

        elif (chosing == '2'):
            yearFrom = int(input('From which year? '))
            yearTo = int(input('To which year? '))
            search = input('What to find?\n')
            result = find_year_by_lunar(search, yearFrom, yearTo)['years']
            print(f'=> {result}') 

        else:
            is_continue=False
            continue

        is_continue=True if input('\n---\nContinue? (yes= 1)\n')=='1' else False
        os.system('cls')
