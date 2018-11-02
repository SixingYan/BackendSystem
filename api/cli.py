#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from gunicorn.app.wsgiapp import WSGIApplication

from moretime.api.wapp import app
from moretime.orm import Facade as orm_facade


@app.shell_context_processor
def shell_context():
    return {'app': app}


def print_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        line = urllib.parse.unquote(
            "{:35s} {:30s} {}".format(rule.rule, methods, rule.endpoint)
        )
        output.append(line)
    for line in sorted(output):
        print(line)


@app.cli.command()
@click.option('--host', default='localhost')
@click.option('--port', type=int, default=8998)
@click.option('--workers', type=int, default=1)
@click.option('--timeout', type=int, default=3600)
def wsgi_server(host, port, workers, timeout):
    wsgi_app = WSGIApplication()
    wsgi_app.load_wsgiapp = lambda: app
    wsgi_app.cfg.set('bind', '%s:%s' % (host, port))
    wsgi_app.cfg.set('workers', workers)
    wsgi_app.cfg.set('timeout', timeout)
    wsgi_app.cfg.set('pidfile', None)
    wsgi_app.cfg.set('accesslog', '-')
    wsgi_app.cfg.set('errorlog', '-')
    wsgi_app.chdir()
    wsgi_app.run()


@app.cli.command()
@click.option('--host', default='localhost')
@click.option('--port', type=int, default=8998)
def debug_server(host, port):
    app.run(host, port)


if __name__ == '__main__':
    debug_server()
