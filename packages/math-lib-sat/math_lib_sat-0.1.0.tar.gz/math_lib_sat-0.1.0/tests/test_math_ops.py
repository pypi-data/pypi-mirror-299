from math_lib_sat.math_ops import MathOps


def test_add_op():
    math_ops = MathOps()
    assert math_ops.add(2, 3), 5
