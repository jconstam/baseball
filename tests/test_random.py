#!/usr/bin/env python3

from baseball.random import D6s

TEST_COUNT = 1000000
DICE_COUNT = 2


def test__roll_one():
    for _ in range(TEST_COUNT):
        results = D6s.roll()
        assert len(results) == 1
        assert results[0] >= 1
        assert results[0] <= 6


def test__rolls():
    for _ in range(TEST_COUNT):
        for count in range(1, DICE_COUNT):
            results = D6s.roll(count)
            assert len(results) == count
            for die in results:
                assert die >= 1
                assert die <= 6