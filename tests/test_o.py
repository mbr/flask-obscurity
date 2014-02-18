import re

from flask_obscurity import obscure
from six import unichr

import pytest


@pytest.fixture
def inp():
    return 'foo@bar.invalid'


@pytest.fixture
def keylen():
    return 5


def _r(s):
    data = s.split(',')

    # load key
    keylength = int(data[0])
    k = [int(i) for i in data[1:1 + keylength]]
    assert len(k) == keylength

    # remainder is "ciphertext"
    ciph = data[1 + keylength:]

    # output
    vals = [0] * (len(ciph) // 2)

    while ciph:
        pos = int(ciph.pop(0))
        byte = int(ciph.pop(0))
        vals[pos] = unichr((byte - k[pos % len(k)]) % 256)

    return ''.join(vals)


def test_2way(inp, keylen):
    assert inp == _r(obscure(inp, keylen))


def test_reasonably_hard_to_read(inp, keylen):
    assert re.match('\d+(?:,\d+)?', obscure(inp, keylen))
