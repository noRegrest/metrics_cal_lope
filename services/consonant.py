import os
import re
from colorama import Fore
from utils import col_txt

def toNH():
    
    is_continue=True

    while is_continue:
        try:  
            os.system('cls')
            text = input("Input: ")

            one_vowel_pattern = r'\b([aeiouyáàảãạăắằẳẵặâấầẩẫậéèẻẽẹêếềểễệíìỉĩịóòỏõọôốồổỗộơớờởỡợúùủũụưứừửữựýỳỷỹỵ])'
            pattern = r'\b(ch|nh|th|ph|kh|gh|ngh|ng|gi|qu|tr|b|c|d|đ|g|h|k|l|m|n|p|q|r|s|t|v|x)'

            def replace(match):
                value = 'nh'+match.group(0)
                return value
            result = re.sub(one_vowel_pattern, replace, text)
            
            def replace_with_nh(match):
                return 'nh'
            result = re.sub(pattern, replace_with_nh, result)
            print()
            print(result)

            is_continue=True if input('\n---\nContinue? (yes)\n')=='' else False
            os.system('cls')
        except Exception as e:
            print(col_txt(fore=Fore.RED,text =  f'{e}'))