#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import toml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def conn(config):
    dbconfig = toml.load('config/mysql.toml')['dev']

    mysql_dsn = 'mysql://{user}:{password}@{host}/{database}?{params}'.format(
        host=dbconfig['host'],
        user=dbconfig['user'],
        password=dbconfig['password'],
        database=dbconfig['database'],
        params=dbconfig['params']
    )

    engine = create_engine(mysql_dsn)
    SessionMaker = sessionmaker(bind=engine)

    return engine, SessionMaker
