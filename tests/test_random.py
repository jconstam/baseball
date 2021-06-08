#!/usr/bin/env python3

import random
import unittest
import unittest.mock

from baseball.random import D6s


class D6Tests(unittest.TestCase):
    def setup_mock(self, side_effects):
        random.randint = unittest.mock.Mock()
        random.randint.side_effect = side_effects

    def test__roll_one(self):
        for i in range(1, 6):
            self.setup_mock([i])
            assert D6s.roll() == [i]
            random.randint.assert_has_calls([unittest.mock.call(1, 6)])

    def test__roll_two(self):
        for i in range(1, 6):
            for j in range(1, 6):
                self.setup_mock([i, j])
                assert D6s.roll(2) == [i, j]
                random.randint.assert_has_calls(
                    [unittest.mock.call(1, 6), unittest.mock.call(1, 6)])
