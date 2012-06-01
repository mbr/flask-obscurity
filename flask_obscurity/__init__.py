#!/usr/bin/env python
# coding=utf8

import random
import os
import re

from jinja2 import Markup, escape
from flask import Blueprint, current_app


class Obscurity(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.blueprint = Blueprint(
            'obscurity',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=self.app.static_url_path + '/oe')

        app.register_blueprint(self.blueprint)
        app.config.setdefault('OBSCURE_KEY_LENGTH', 5)

        app.jinja_env.filters['pmailto'] = pmailto
        app.jinja_env.filters['pspan'] = pspan
        app.jinja_env.filters['pmailto_all'] = pmailto_all
        app.jinja_env.filters['pspan_all'] = pspan_all


EMAIL_REGEX = re.compile(
   "[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z"\
   "0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?"
)


def obscure(address, keylength=None):
    if not keylength:
        keylength = current_app.config['OBSCURE_KEY_LENGTH']
    k = [ord(c) for c in key]

    positions = range(len(address))
    random.shuffle(positions)

    # format: key length, key bytes, [pos, byte]
    rv = [len(k)]
    rv.extend(k)
    for pos in positions:
        rv.append(pos)
        rv.append((ord(address[pos])+k[pos%len(k)])%256)
        k[pos%len(key)]

    return ','.join(str(n) for n in rv)


def pmailto(address, key=None):
    return Markup(
        u'<a class="oe-link" data-oe="%s">(hidden email address)</a>' %\
           escape(obscure(address, key))
    )


def pspan(address, key=None):
    return Markup(
        u'<span class="oe-span" data-oe="%s">(hidden email address)</a>' %\
           escape(obscure(address, key))
    )


def pmailto_all(text, key=None):
    return EMAIL_REGEX.sub(lambda m: pmailto(m.group(0)), text)


def pspan_all(text, key=None):
    return EMAIL_REGEX.sub(lambda m: pspan(m.group(0)), text)
