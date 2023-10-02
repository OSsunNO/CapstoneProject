import re
import argparse
import os
from datetime import datetime

pattern_dict = {
    "res_num_with_dash": {
        "pattern": r"\b(\d{2})([0-1][0-9])([0-3][0-9])-([1-4])\d{6}\b",
        "type": "주민등록번호",
        "replacement": "******-*******"
    },
    "res_num_without_dash": {
        "pattern": r"\b(\d{2})([0-1][0-9])([0-3][0-9])([1-4])\d{6}\b",
        "type": "주민등록번호",
        "replacement": "*************"
    },
    "phone_num_with_dash": {
        "pattern": r'010-\d{4}-\d{4}',
        "type": "전화번호",
        "replacement": "010-****-****"
    },
    "phone_num_without_dash": {
        "pattern": r'010\d{8}',
        "type": "전화번호",
        "replacement": "010********"
    },
     "email": {
        "pattern": r'\b([\w.%+-]+)@([\w.-]+\.[a-zA-Z]{2,})\b',
        "type": "이메일 주소",
        "replacement": lambda match: '*' * len(match.group(1)) + '@' + match.group(2)
    },
    "company_num_with_dash": {
        "pattern": r'\b\d{3}-\d{2}-\d{5}\b',
        "type": "사업자 등록번호",
        "replacement": "***-**-*****"
    },
    "company_num_without_dash": {
        "pattern": r'\b\d{10}\b',
        "type": "사업자 등록번호",
        "replacement": "**********"
    },
    "address": {
    "pattern": r"((\b[가-힣]+구\b)[\s\w~\-.]*(\d{1,5}([~\-]\d{1,5})?))",
    "type": "주소",
    "replacement": lambda m: m.group(2) + ' ' + '*' * (len(m.group(3)) - m.group(3).count('-'))
    }

}

def is_valid_date(year, month, day):
    try:
        datetime(year, month, day)
        return True
    except ValueError:
        return False
    

def run(fileName):
    print("---Personal data detection module processing---")

    # Find input file from database directory
    db_dir = os.path.join("..", "database")
    file_dir = os.path.join(db_dir, fileName)
    print(file_dir)

    # Replace and save as new file
    newFileName = fileName.replace(".txt", "_filtered.txt")
    new_file_dir = os.path.join(db_dir, newFileName)
    with open(new_file_dir, "w+", encoding='utf-8') as nf:
        with open(file_dir, "r", encoding='utf-8') as f:
            for line in f:
                target=line.strip()

                for pattern in pattern_dict:
                   match = re.search(pattern_dict[pattern]["pattern"], target)  
                   if match:
                        print(f'{pattern_dict[pattern]["type"]} detected on target sentence:')
                        print(f"{target}")
                        # 주민등록번호 패턴이라면
                        if "res_num" in pattern:
                            year = 1900 + int(match.group(1)) if match.group(4) in ['1', '2'] else 2000 + int(match.group(1))
                            month, day = int(match.group(2)), int(match.group(3))
                        
                            # 유효한 날짜인지 확인하고 아니면 continue
                            if not is_valid_date(year, month, day): continue

                        
                        target = re.sub(pattern_dict[pattern]["pattern"], pattern_dict[pattern]["replacement"], target)

                nf.write(target+'\n')
        f.close()
    nf.close()