#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class Facade(object):
    Engine = None
    SessionMaker = None

    DefaultHost = 'localhost'
    DefaultUser = 'root'
    DefaultPassword = '123456ysx'
    DefaultPort = 3306
    DefaultDB = 'moremom'

    @staticmethod
    def initialize(d_config):
        mysql_dsn = 'mysql://{user}:{password}@{host}:{port}/{db}?{params}'.format(
            host=d_config.get('host', Facade.DefaultHost),
            port=d_config.get('port', Facade.DefaultPort),
            user=d_config.get('user', Facade.DefaultUser),
            password=d_config.get('password', Facade.DefaultPassword),
            db=d_config.get('db', Facade.DefaultDB),
            params=d_config.get('params', '')
        )
        Facade.Engine = create_engine(mysql_dsn)
        Facade.SessionMaker = sessionmaker(bind=Facade.Engine)

    @staticmethod
    def make_session():
        return Facade.SessionMaker()

    @staticmethod
    def make_scoped_session():
        return scoped_session(Facade.SessionMaker)

    @staticmethod
    def release_session(session):
        session.remove()
