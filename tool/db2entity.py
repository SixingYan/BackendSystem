#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import getpass

import jinja2
from sqlalchemy import create_engine
from sqlalchemy import MetaData


class ArgsPassword(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-p', '--port', help='mysql port', type=int, default=3306)
parser.add_argument('-H', '--host', help='mysql host', type=str, default='localhost')
parser.add_argument('-d', '--db', help='database', type=str, default='moremom')
parser.add_argument('-t', '--table', help='table', type=str, default='')
parser.add_argument('-u', '--user', help='user', type=str, default='root')
parser.add_argument('-P', '--password', action=ArgsPassword, nargs='?', dest='password', help='Password', default='123456ysx')
args = parser.parse_args()

target_tables = []
if args.table:
    target_tables = [args.table]
if ',' in args.table:
    target_tables = args.table.split(',')


mysql_dsn = 'mysql://{user}:{password}@{host}:{port}/{database}'.format(
    host=args.host,
    user=args.user,
    port=args.port,
    password=args.password,
    database=args.db
)

try:
    engine = create_engine(mysql_dsn, echo=False)
    metadata = MetaData()
    metadata.reflect(bind=engine)
except Exception as e:
    print(e)
    exit()


def inception_class_name_from_table_name(table_name):
    return ''.join(t[0].upper() + t[1:] for t in table_name.split('_'))


def column_python_type(col) -> str:
    python_type = col.type.python_type
    return python_type.__name__


tables = []
ignore_columns = ['status', 'create_ts', 'update_ts']
for table_name, table in metadata.tables.items():
    if target_tables and table_name not in target_tables:
        continue
    table.inception_class_name = inception_class_name_from_table_name(table.name)
    table.my_columns = []
    for c in table.columns:
        if c.name in ignore_columns:
            continue
        c.s_python_type = column_python_type(c)
        table.my_columns.append(c)
    tables.append(table)

SCHEMA_TEMPLATE = '''#!/usr/bin/env python3\n# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal


{%for table in tables %}
class {{table.inception_class_name}}({{base}}):
    def __init__(self, {% for col in table.my_columns %}{% if loop.last %}{{col.name}}{% else %}{{col.name}}, {% endif %}{% endfor %}):
{% for col in table.my_columns %}
        self.{{col.name}} = {{col.name}}
{% endfor %}

    @classmethod
    def default(cls):
        instance = {{table.inception_class_name}}(
{% for col in table.my_columns %}
            {{col.name}}={{col.s_python_type}}(),
{% endfor %}
        )
        return instance

    @classmethod
    def from_dict(cls, d):
        instance = {{table.inception_class_name}}(
{% for col in table.my_columns %}
            {{col.name}}=d[\'{{col.name}}\'],
{% endfor %}
        )
        return instance

    @classmethod
    def from_object(cls, o):
        instance = {{table.inception_class_name}}(
{% for col in table.my_columns %}
            {{col.name}}=getattr(o, '{{col.name}}'),
{% endfor %}
        )
        return instance


{% endfor %}
'''

template = jinja2.Template(SCHEMA_TEMPLATE, trim_blocks=True)
inception_code = template.render(
    base='object',
    tables=tables
)

i = -1
while i > -len(inception_code) - 1:
    if inception_code[i] == '\n':
        i -= 1
    else:
        break
if i == -1:
    inception_code = inception_code + '\n'

inception_code = inception_code[0:i + 2]

print(inception_code, end='')
