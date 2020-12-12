#!/usr/bin/env python3
import csv

from bs4 import BeautifulSoup
import re
from pprint import pprint


def get_all_records(html_file):
    records = {}
    soup = BeautifulSoup(html_file, 'html.parser')
    check = False
    check_task_number = False
    for _ in soup.find_all(id=re.compile(r'rec\d+')):
        if not check:
            if ' '.join(_['class']) == 'r t-rec t-rec_pt_0 t-rec_pb_0':
                check = True
            else:
                continue

        temp = _.find_all(name='div', attrs={'class': 'tn-atom'})
        if len(temp) == 3:
            task = re.findall(r'\d+', str(temp[0].contents[0]))[0]
            contents = '\n'.join(temp[2].strings)
            if check_task_number:
                records[f'2.{task}'] = contents
            else:
                if task == '1' and task in records:
                    check_task_number = True
                    records[f'2.{task}'] = contents
                    continue
                records[task] = contents
            continue

        temp = _.find(name='div', attrs={'class': 't004'})
        if temp is not None:
            task = re.findall(r'\d+', str(temp.find(name='div', attrs={'field': 'text'}).strong.contents[0]))[0]
            # contents = str(temp.find(name='div', attrs={'field': 'text'}).find_all('span')[-1].string)
            contents = str(temp.find(name='div', attrs={'field': 'text'}).find_all('span')[-1].string)
            if check_task_number:
                records[f'2.{task}'] = contents
            else:
                if task == '1' and task in records:
                    check_task_number = True
                    records[f'2.{task}'] = contents
                    continue
                records[task] = contents

    return records


def write_file(name):
    with open("html_doc.html", 'r') as file:
        html_doc = file.read()
    print('File is creating')
    all_records = get_all_records(html_doc)

    with open(f'{name}.csv', 'w') as file:
        writer = csv.writer(file)
        for key, val in all_records.items():
            writer.writerow((key, val))
            # file.write(f'{key}:\n{val}\n\n')
    return 'Hello write_file'