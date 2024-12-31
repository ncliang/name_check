#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs
import re
import urllib.error
import urllib.parse
import urllib.request

import requests

NAME_TEMPLATE = '%s%s%s'
CHECK_NAME_URL_TEMPLATE = 'http://www.123cha.com/xm/%s-0'
REGEX = '得分:(\d+)'
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
    url = get_url(name_to_check)
    try:
        resp = requests.get(url, timeout=2)
    except Exception:
        return None
    page_content = resp.text
    m = re.search(REGEX, page_content)
    if m is not None:
        return m.group(1)
    return None


def get_url(name):
    return CHECK_NAME_URL_TEMPLATE % urllib.parse.quote(name.encode('utf-8'))


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
    url = get_url(name)
    score = get_score(name)
    print('(%s, %s, %s)' % (score, name, url))
    outputs.append((score, name, url))
    # time.sleep(0.5)

outputs.sort(reverse=True)
with codecs.open(args.output, 'w', encoding='utf-8') as out_file:
    for score, name, url in outputs:
        out_file.write('(%s, %s, %s)\n' % (score, name, url))
