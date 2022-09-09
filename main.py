from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
import requests
import gspread
import time
import csv

paper_title = []
authors = []
sentences_before_clean = []
sentences_after_clean = []
url = []

# User Agent.
headers = {'User-Agent': '''Put your user agent here.'''}





links =[
"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8839149/",

]

for link in links:
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Getting the URL.
    url.append(link)

    # Getting the paper title.
    paper_title.append(soup.find('h1').get_text())

    # Getting the authors.
    author = authors.append(', '.join([author.get_text() for author in soup.find('div', class_='contrib-group fm-author').findAll('a')]))


    #Getting the BIOXcell indexing.
    paragraphs = [paragraph.get_text() for paragraph in soup.findAll('p')]
    for paragraph in paragraphs:
        if 'Bio-X-Cell' in paragraph or 'Bioxcell' in paragraph or 'bioxcell' in paragraph or 'Bio X Cell' or 'Bioxcell)' in paragraph or '(Bioxcell' in paragraph or 'BioXcell' in paragraph:

            # Splitting the words.
            words = paragraph.split()

            # Word index is ending point.
            word_index = [indx for (indx, word) in enumerate(words) if word.strip("().;,").lower() == "bioxcell" or word.strip("().;,").lower() == "bio-x-cell" or word.strip("().;,").lower() == "bio x cell" or word == '(Bio-X-Cell)' or word.strip('),')[-8:] == 'BioXcell' or word.strip(').')[-8:] == 'BioXcell' or word.strip(')')[-8:] == 'BioXcell' or word.strip(').').lower()[-8:] == 'bioxcell' or word.strip('(),')[:10] == 'Bio-X-Cell' or word.strip('().') == 'BioXcell' or word.lower().strip('[],') == 'bioxcell' or word == '(Bio-X-Cell,' or word[1:11] == 'Bio-X-Cell' or word.strip('(,') == 'Bio‐X‐Cell' and indx > 0]
            # print("Word index")
            # print(word_index)                                                                        
            # print('\n')
            #Getting the dots at the words.
            dot_index = [indx for indx,word in enumerate(words) if word.endswith(".")][::-1]
            # print(dot_index)

            # Extracting the sentences.
            lst = []
            # Starting point.

            count = 0
            while count < len(word_index):
                for number in dot_index:
                    if (word_index[count] - dot_index[dot_index.index(number)]) >= 7:
                        lst.append(dot_index[dot_index.index(number)])
                        break
                    else:
                        continue
                count += 1
            lst = set(lst)
            lst = list(lst)
            lst.sort()
            # print("Nearest point")
            # print(lst)
            # print('\n')
            
            #Looping throw all words in paragraph to print the sentence.
            for i in range(len(word_index)):
                if not lst:
                    sentences_before_clean.append(" ".join(words[:word_index[-1]+1]).strip(',;') + ".")
                    break
                elif len(word_index) > len(lst):
                    sentences_before_clean.append(" ".join(words[lst[0]+1:word_index[-1]+1]))
                    # print('2')
                    break
                # elif lst.count(lst[0]) == len(lst):
                #     sentences.append(" ".join(words[lst[0]+1:word_index[-1]+1]))
                #     print('2')
                else:
                    sentences_before_clean.append(" ".join(words[lst[i]+1:word_index[i]+1]).strip(',;') + ".")
                    sentences_before_clean = set(sentences_before_clean)
                    sentences_before_clean = list(sentences_before_clean)
                    # print('3')
# Check if the word Semen is exit or not.

    # Getting the data in tables.        
    table_data = [(table_raw.get_text() + ".")  for table_raw in soup.findAll('tr') if 'Bio-x-cell' in table_raw.get_text() or 'BioxCell' in table_raw.get_text() or 'bioxcell' in table_raw.get_text() or 'Bio-X-Cell' in table_raw.get_text() or '(Bio-x-Cell' in table_raw.get_text() or '(Bio-x-Cell)' in table_raw.get_text() or 'Bio-x-Cell)' in table_raw.get_text() or 'BioXcell' in table_raw.get_text() or 'BioXCell' in table_raw.get_text() or 'BIO-X-CELL' in table_raw.get_text() or 'Bioxcell' in table_raw.get_text()]
    for table in table_data:
        sentences_before_clean.append(table)   

    # Getting the data in tag list.
    data_in_list = [(lst.get_text()) for lst in soup.findAll('li')]
    split_lst = [lst.split() for lst in data_in_list]
    for lst1 in split_lst:
        for word in lst1:
            if len(lst1) > 65:
                continue
            elif word.lower().strip('().;[],') == 'bioxcell' or word.lower().strip('().;[],') == 'bio-x-cell' or word.lower().strip('().;[],') == 'bio x cell' or word.strip('();').lower()[-8:] == 'bio-x-cell' or word.strip('();').lower()[:10] == 'bio-x-cell' or word.strip('(;') == 'Bio-X-Cell':
                sentences_before_clean.append(' '.join(lst1))
                break

    l1 = paper_title
    l2 = authors
    l3 = '###'.join(sentences_before_clean)
    # l4 = sentences_after_clean
    l5 = url

    s1 = pd.Series(l1, name='Paper title')
    s2 = pd.Series(l2, name='Authours')
    s3 = pd.Series(l3, name='Sentences before clean')
    # s4 = pd.Series(l4, name='Sentences after clean')
    s5 = pd.Series(l5, name ='URL')
    df = pd.concat([s1, s2, s3, s5], axis=1)
    df.to_csv('example_01.csv', index=False)

print("Done")