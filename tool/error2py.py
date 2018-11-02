#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import re
import yaml

from jinja2 import Template


def hump2underline(hunp_str):
    '''
    驼峰形式字符串转成下划线形式
    :param hunp_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    '''
    # 匹配正则，匹配小写字母和大写字母的分界位置
    p = re.compile(r'([a-z]|\d)([A-Z])')
    # 这里第二个参数使用了正则分组的后向引用
    sub = re.sub(p, r'\1_\2', hunp_str).lower()
    return sub


parser = argparse.ArgumentParser(add_help=True)
parser = argparse.ArgumentParser()
# parser.add_argument('input_file')
parser.add_argument('-o', '--output', type=str,
                    default='/Users/alfonso/workplace/moretime/wrong/error.py')
args = parser.parse_args()

input_file = '/Users/alfonso/workplace/moretime/docs/error.yaml'
# input_file = args.input_file
mylist = yaml.load(open(input_file, encoding='utf-8'))

code_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Define API Errors

    An API error object is an instance of `namedtuple`.
"""

from collections import namedtuple

APIError = namedtuple("APIError", ["code", "msg", "wording"])

{% for k,v in mylist.items() -%}
{{k}} = APIError({{ v.code }}, "{{ v.message }}", "{{ v.wording }}")
{% endfor %}
'''

template = Template(code_content)
code_content = template.render(mylist=mylist)

i = -1
while i > -len(code_content) - 1:
    if code_content[i] == '\n':
        i -= 1
    else:
        break
if i == -1:
    code_content = code_content + '\n'
if i < -2:
    code_content = code_content[0:i + 2]

with open(args.output, "w", encoding="utf-8") as fd:
    fd.write(code_content)
