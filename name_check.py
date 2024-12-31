#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs

import requests
from lxml import etree

NAME_TEMPLATE = '%s%s%s'
URL = 'https://www.zhanbuwang.com/xingmingceshi_2.php'
XPATH = '/html/body/div/div/div[3]/div[2]/div/div[2]/div[1]/span'
SKIP_CHARS = {
    '　', '：', '（', '）', ' ', '；', '，', '。', '「', '」', '\n', 'ˋ'
}

parser = argparse.ArgumentParser(description='Generate some name candidates.')
parser.add_argument('--family-name', default='梁', help='Family name to use in generation')
parser.add_argument('--middle-character', help='Optional fixed middle character')
parser.add_argument('--text',
                    help='Path to text file used for name generation. Must be utf-8 encoded',
                    required=True)
parser.add_argument('--output', help='Path to text file used as output', default='output.txt')

args = parser.parse_args()

with codecs.open(args.text, encoding='UTF-8') as input:
    inputs = input.readlines()

inputs = ''.join(inputs)
deduped_inputs = set(inputs)
deduped_inputs -= SKIP_CHARS
print('Number of characters to try: %s' % len(deduped_inputs))


def get_score(name_to_check):
    last_name = name_to_check[0]
    first_name = name_to_check[1:]

    form_data = {
        "nametype": "1231",
        "pf_xing": last_name,
        "pf_ming": first_name,
        "submit": "名字測試打分"
    }

    try:
        resp = requests.post(URL, data=form_data)
    except Exception:
        return None
    page_content = resp.text
    tree = etree.HTML(page_content)
    try:
        return tree.xpath(XPATH)[0].text
    except IndexError:
        return None


def name_generator():
    for last_char in deduped_inputs:
        if args.middle_character is None:
            for middle_char in deduped_inputs:
                if middle_char == last_char:
                    continue

                yield NAME_TEMPLATE % (args.family_name, middle_char, last_char)
        else:
            yield NAME_TEMPLATE % (args.family_name, args.middle_character, last_char)


outputs = []
for name in name_generator():
    score = get_score(name)
    print('(%s, %s)' % (score, name))
    outputs.append((score, name))
    # time.sleep(0.5)

outputs.sort(reverse=True)
with codecs.open(args.output, 'w', encoding='utf-8') as out_file:
    for score, name in outputs:
        out_file.write('(%s, %s)\n' % (score, name))
