from flask import Flask, render_template
from flask_obscurity import Obscurity
from jinja2 import FunctionLoader

import pytest


tpl = {
    'single.html': """test {{addr|pmailto}} it""",
    'singlenolink.html': """test inside {{addr|pspan}} all""",
    'par.html': """{{('hello ' + addr + ' world')|pmailto_all}}""",
    'parnolink.html': """{{('hello ' + addr + ' world')|pspan_all}}""",
}


def load_template(name):
    return tpl.get(name, None)


@pytest.fixture
def app():
    app = Flask(__name__)
    app.jinja_loader = FunctionLoader(load_template)

    Obscurity(app)

    return app


@pytest.fixture(params=['foo@bar.invalid', 'test@asdf.com',
                        'stramge@foo.bar.de', 'foo.bar.baz@12.12.12.12'])
def addr(request):
    return request.param


@pytest.fixture(params=tpl.keys())
def template(request):
    return request.param


def test_basics(app, addr, template):
    with app.app_context():
        buf = render_template(template, addr=addr)
        assert addr not in buf
