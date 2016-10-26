import pickle
from math import log as math_log

from nose.tools import eq_

from .. import modifiers
from ...dependencies import solve


def test_log():
    log_five = modifiers.log(5)

    eq_(solve(log_five), math_log(5))

    eq_(solve(pickle.loads(pickle.dumps(log_five))), math_log(5))

    eq_(repr(log_five), "<feature.log(5)>")


def test_max():

    max_five_six_seven = modifiers.max(5, 6, 7)

    eq_(solve(max_five_six_seven), 7)

    eq_(solve(pickle.loads(pickle.dumps(max_five_six_seven))), 7)

    eq_(repr(max_five_six_seven), "<feature.max(5, 6, 7)>")


def test_min():

    min_five_six_seven = modifiers.min(5, 6, 7)

    eq_(solve(min_five_six_seven), 5)

    eq_(pickle.loads(pickle.dumps(min_five_six_seven)), min_five_six_seven)

    eq_(repr(min_five_six_seven), "<feature.min(5, 6, 7)>")
