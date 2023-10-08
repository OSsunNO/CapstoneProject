import pandas as pd
import os
import time
import emoji
import re


def run(fileName):
    
    print("---Special character replacing module processing---")
    
    # file reading start
    start_of_read_file = time.time()
    
    # Read Excel and save to ../database/fake.txt
    test_data = pd.read_excel("../database/largedata_1.xlsx")
    with open("../database/demo.txt", "w", encoding='utf-8') as fd:
      for t in test_data['sentence']:
            line = t.split('\n')
            for l in line:
                  fd.write(l+'\n')
    fd.close()
    
    # file reading end
    end_of_read_file = time.time()
    
    print(f"Excel reading time: {end_of_read_file-start_of_read_file:.5f} sec")
    
    # module processing start
    start_of_module = time.time()

    # Read emoticon_dict
    emoticon_dict = pd.read_excel("modules/spc/spc_dict_v2.xlsx")

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
                
                detected_colon=[':']*target.count(':')
                if(len(detected_colon)!=0):
                    # pass
                    print(f"detected_spc: {detected_colon}, converted_text_form: '', desc: spc") # print out the log
                target=target.replace(':','')
                    
                
                # EMOJI
                a=list(emoji.analyze(target))
                for i in range(len(a)):
                    
                    detected_emoji = a[i].chars
                    converted_text_form = emoji.demojize(detected_emoji, language='ko')
                    
                    # print out detected_emoji and converted_text_form
                    print(f"detected_emoji: {detected_emoji}, converted_text_form: {converted_text_form}, desc: emoji") # print out the log
                    
                # let emoji convert into text form
                target=emoji.demojize(target, language='ko')
                
                # EMOTICON
                for e, c in zip(emoticon_dict['emoticon'], emoticon_dict['category']):
                    if e in target:
                        print(f"detected_emoticon: {e}, converted_text_form: {c}, desc: emoticon")  # print out the log
                        target = target.replace(e, ':'+c+':')  # replace the emoticon with ':category:' form
                
                
                # 1-digit SPC
                special=re.compile(r'[^\sㄱ-ㅣA-Za-z0-9가-힣:+]')
                # find 1-digit special character in target sentence
                detected_spc = special.findall(target)
                if(len(detected_spc)!=0):
                    # pass
                    print(f"detected_spc: {detected_spc}, converted_text_form: '', desc: spc")
                # remove 1-digit special character
                target=special.sub('',target)
                nf.write(target+'\n')
        f.close()
    nf.close()
    
    # module processing end
    end_of_module = time.time()
    
    print(f"Running time of spc module: {end_of_module-start_of_module:.5f} sec")
