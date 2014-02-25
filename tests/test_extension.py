from flask import Flask, render_template
from flask_obscurity import Obscurity, pmailto_all
from jinja2 import FunctionLoader

import pytest


tpl = {
    'single.html': """test {{addr|pmailto}} it""",
    'singlenolink.html': """test inside {{addr|pspan}} all""",
    'par.html': """{{('hello ' + addr + ' world')|pmailto_all}}""",
    'parnolink.html': """{{('hello ' + addr + ' world')|pspan_all}}""",
    'header.html': """{{obscurity_js()}}"""
}


def load_template(name):
    return tpl.get(name, None)


@pytest.fixture
def app():
    app = Flask(__name__)
    app.jinja_loader = FunctionLoader(load_template)

    Obscurity(app)

    return app


@pytest.fixture
def client(app):
    app.testing = True
    return app.test_client()


@pytest.fixture(params=['foo@bar.invalid', 'test@asdf.com',
                        'stramge@foo.bar.de', 'foo.bar.baz@12.12.12.12'])
def addr(request):
    return request.param


@pytest.fixture(params=tpl.keys())
def template(request):
    return request.param


def test_basics(app, addr, template):
    with app.test_request_context():
        buf = render_template(template, addr=addr)
        assert addr not in buf


def test_js(client):
    rv = client.get('/static/oe/js/uoe.js')
    assert rv.status_code == 200


def test_js_include(app):
    with app.test_request_context():
        buf = render_template('header.html')
        assert '/static/oe/js/uoe.js' in buf


def test_mailto_replaces_properly_simple(addr, app):
    with app.app_context():
        text = 'some text ' + addr + ' more'
        assert addr not in pmailto_all(text)


def test_mailto_replaces_propery_end_of_sentence(addr, app):
    with app.app_context():
        text = 'long sentence with stuff ' + addr + '.'
        assert addr not in pmailto_all(text)
