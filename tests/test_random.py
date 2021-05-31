#!/usr/bin/env python3

from baseball.random import D6s

TEST_COUNT = 1000000


def test__one_range():
    for _ in range(TEST_COUNT):
        val = D6s.roll_one()
        assert val >= 1
        assert val <= 6


def test__two_range():
    for _ in range(TEST_COUNT):
        val = D6s.roll_two()
        assert val >= 1
        assert val <= 12
