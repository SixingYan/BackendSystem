#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import getpass
import re

import jinja2

from sqlalchemy import create_engine, MetaData
from sqlalchemy.sql.schema import DefaultClause


class ArgsPassword(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()
        setattr(namespace, self.dest, values)


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-p', '--port', help='mysql port', type=int, default=3306)
parser.add_argument('-H', '--host', help='mysql host', type=str, default='47.94.101.97')
parser.add_argument('-d', '--db', help='database', type=str, default='moremom')
parser.add_argument('-t', '--table', help='table', type=str, default='')
parser.add_argument('-u', '--user', help='user', type=str, default='db')
parser.add_argument('-P', '--password', action=ArgsPassword, nargs='?', dest='password', help='Password', default='MoreAf_3f+X8_3hO')
parser.add_argument('-b', '--base', help='use base model class or not', type=int, default=1)
parser.add_argument('-a', '--args', help='args', type=str, default='charset=utf8mb4')
args = parser.parse_args()

use_base = args.base

target_tables = []
if args.table:
    target_tables = [args.table]
if ',' in args.table:
    target_tables = args.table.split(',')


mysql_dsn = 'mysql://{user}:{password}@{host}:{port}/{database}?{args}'.format(
    host=args.host,
    user=args.user,
    port=args.port,
    password=args.password,
    database=args.db,
    args=args.args,
)

try:
    engine = create_engine(mysql_dsn, echo=False)
    metadata = MetaData()
    metadata.reflect(bind=engine)
except Exception as e:
    print(e)
    exit()


def model_class_name_from_table_name(table_name):
    return ''.join(t[0].upper() + t[1:] for t in table_name.split('_')) + 'Model'


def default_clause_repr(c):
    t = c.arg.text
    if len(t) == 2 and t[0] == "'" and t[-1] == "'":
        text = 'DefaultClause(TextClause("\'\'"))'
    elif len(t) > 0 and t[0] == "'" and t[-1] == "'":
        text = 'DefaultClause(TextClause(%s))' % c.arg.text
    else:
        text = 'DefaultClause(TextClause(\'%s\'))' % c.arg.text
    return text


def my_repr(obj):
    if isinstance(obj, DefaultClause):
        return default_clause_repr(obj)
    return repr(obj)


def column_expr(col):
    kwarg = []
    if col.key != col.name:
        kwarg.append('key')
    if col.primary_key:
        kwarg.append('primary_key')
    if not col.nullable:
        kwarg.append('nullable')
    if col.default:
        kwarg.append('default')
    if col.server_default:
        kwarg.append('server_default')
    if col.comment:
        kwarg.append('comment')
    expr = "Column(%s)" % ', '.join(
        [repr(col.name)] + [repr(col.type)] +
        [repr(x) for x in col.foreign_keys if x is not None] +
        [repr(x) for x in col.constraints] +
        ["%s=%s" % (k, my_repr(getattr(col, k))) for k in kwarg]
    )
    expr = re.sub(r"collation='.*', ", '', expr)
    expr = re.sub(r"charset='.*', ", '', expr)
    return expr


def index_expr(idx):
    expr = 'Index(%s)' % (
        ", ".join(
            [repr(idx.name)] +
            [column_expr(e) for e in idx.expressions] +
            (idx.unique and ["unique=True"] or [])
        ))
    expr = re.sub(r"collation='.*', ", '', expr)
    expr = re.sub(r"table=<.*>", '', expr)
    return expr


tables_for_model = []
for table_name, table in metadata.tables.items():
    if target_tables and table_name not in target_tables:
        continue

    table.model_class_name = model_class_name_from_table_name(table.name)
    for c in table.columns:
        c.repr_ = column_expr(c)
    for i in table.indexes:
        i.repr_ = index_expr(i)
    tables_for_model.append(table)


SCHEMA_TEMPLATE = '''#!/usr/bin/env python3\n# -*- coding: utf-8 -*-

from sqlalchemy import Column, Index
from sqlalchemy.dialects.mysql import \\
    TINYINT, SMALLINT, INTEGER, BIGINT, \\
    VARCHAR, TEXT, \\
    DECIMAL, NUMERIC, \\
    TIMESTAMP, DATE, DATETIME
from sqlalchemy.sql.schema import DefaultClause
from sqlalchemy.sql.elements import TextClause


_ = TINYINT
_ = SMALLINT
_ = INTEGER
_ = BIGINT
_ = VARCHAR
_ = TEXT
_ = DECIMAL
_ = NUMERIC
_ = TIMESTAMP
_ = DATE
_ = DATETIME


{% if use_base_model == 0 %}
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
{% else %}
from sqlalchemy.ext.declarative import as_declarative
import ast
import time

@as_declarative()
class Base(object):

    def fields(self):
        fields = dict()
        for column in self.__table__.columns:
            fields[column.name] = getattr(self, column.name)
        return fields

    def keys(self):
        columns = self.__table__.columns
        return tuple([c.name for c in columns])

    def add(self, session_):
        return session_.add(self)

    def update(self, fields):
        for column in self.__table__.columns:
            if column.name in fields:
                setattr(self, column.name, fields[column.name])

    def to_dict(self):
        d = {k: v for k, v in vars(self).items() if not k.startswith('_')}
        return str(d)

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            data = ast.literal_eval(data)
        id = None
        if "id" in data:
            id = data.pop("id")

        o = cls(**data)
        o.id = id
        return o

    @classmethod
    def get(cls, id_, session_):
        return session_.query(cls).get(id_)

    @classmethod
    def query(cls, session_):
        return session_.query(cls)

    @classmethod
    def query_id(cls, session_):
        return session_.query(cls.id)

    @classmethod
    def local_ts(cs):
        return int(time.mktime(time.localtime()))
{% endif %}


{%for table in tables %}
class {{table.model_class_name}}({{base}}):
    __tablename__ = '{{table.name}}'
{% for col in table.columns %}
    {{col.name}} = {{col.repr_}}
{% endfor %}
{% if table.indexes %}
    __table_args__ = (
{% for idx in table.indexes %}
        {{idx.repr_}},
{% endfor %}
    )
{% endif %}


{% endfor %}
'''

template = jinja2.Template(SCHEMA_TEMPLATE, trim_blocks=True)
model_define_code = template.render(
    base='Base',
    tables=tables_for_model,
    use_base_model=use_base
)

i = -1
while i > -len(model_define_code) - 1:
    if model_define_code[i] == '\n':
        i -= 1
    else:
        break
if i == -1:
    model_define_code = model_define_code + '\n'

model_define_code = model_define_code[0:i + 2]

print(model_define_code, end='')
