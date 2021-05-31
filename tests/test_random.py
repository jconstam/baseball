#!/usr/bin/env python3

from baseball.random import D6s


def test__one_range():
    for _ in range(100000):
        val = D6s.roll_one()
        assert val >= 1
        assert val <= 6
