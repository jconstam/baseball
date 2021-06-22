#!/usr/bin/env python3

import unittest
import unittest.mock

import baseball.random

from baseball.pitcher import Pitcher, PITCH_RESULT


class PitcherTestBase(unittest.TestCase):
    def setup_mock(self, side_effects):
        baseball.random.D6s = unittest.mock.Mock()
        baseball.random.D6s.roll.side_effect = side_effects


class PitcherExceptionTests(PitcherTestBase):
    def validate_exception_with_message(self, exception, message, function, *args, **kwargs):
        try:
            function(*args, **kwargs)
            self.assertFalse()
        except Exception as ex:
            self.assertIsInstance(ex, exception)
            self.assertEqual(ex.args[0], message)

    def test__pitch_roll_invalid_results_none(self):
        self.setup_mock([None])
        self.validate_exception_with_message(
            AssertionError, 'Invalid pitch: None', Pitcher.run_next_action)

    def test__pitch_roll_invalid_results_int(self):
        self.setup_mock([1])
        self.validate_exception_with_message(
            AssertionError, 'Invalid pitch: 1', Pitcher.run_next_action)

    def test__pitch_roll_no_results(self):
        self.setup_mock([[]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid pitch size: []', Pitcher.run_next_action)

    def test__pitch_roll_too_many_results(self):
        self.setup_mock([[1, 2]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid pitch size: [1, 2]', Pitcher.run_next_action)

    def test__pitch_roll_invalid_result_low(self):
        self.setup_mock([[0]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid pitch at 0: 0', Pitcher.run_next_action)

    def test__pitch_roll_invalid_result_high(self):
        self.setup_mock([[7]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid pitch at 0: 7', Pitcher.run_next_action)

    def test__swing_roll_invalid_results_none(self):
        self.setup_mock([[1], None])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing: None', Pitcher.run_next_action)

    def test__swing_roll_invalid_results_int(self):
        self.setup_mock([[1], 1])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing: 1', Pitcher.run_next_action)

    def test__swing_roll_no_results(self):
        self.setup_mock([[1], []])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing size: []', Pitcher.run_next_action)

    def test__swing_roll_not_enough_results(self):
        self.setup_mock([[1], [1]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing size: [1]', Pitcher.run_next_action)

    def test__swing_roll_too_many_results(self):
        self.setup_mock([[1], [1, 2, 3]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing size: [1, 2, 3]', Pitcher.run_next_action)

    def test__swing_roll_invalid_first_result_low(self):
        self.setup_mock([[1], [0, 1]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing at 0: 0', Pitcher.run_next_action)

    def test__swing_roll_invalid_first_result_high(self):
        self.setup_mock([[1], [7, 1]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing at 0: 7', Pitcher.run_next_action)

    def test__swing_roll_invalid_second_result_low(self):
        self.setup_mock([[1], [1, 0]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing at 1: 0', Pitcher.run_next_action)

    def test__swing_roll_invalid_second_result_high(self):
        self.setup_mock([[1], [1, 7]])
        self.validate_exception_with_message(
            AssertionError, 'Invalid swing at 1: 7', Pitcher.run_next_action)


class PitcherTests(PitcherTestBase):
    def check_result(self, side_effects, result):
        self.setup_mock(side_effects)
        assert Pitcher.run_next_action() == result
        calls = [unittest.mock.call()]
        for i in range(1, len(side_effects)):
            calls.append(unittest.mock.call(2))
        baseball.random.D6s.roll.assert_has_calls(calls)

    def test__run_next_action__swing(self):
        for i in range(1, 5):
            self.check_result([[i], [1, 1]], PITCH_RESULT.DOUBLE__2_BASE)
            self.check_result(
                [[i], [1, 2]], PITCH_RESULT.GROUND_OUT__DOUBLE_PLAY)
            self.check_result([[i], [1, 3]], PITCH_RESULT.HIT_BY_PITCH)
            self.check_result([[i], [1, 4]], PITCH_RESULT.SINGLE__1_BASE)
            self.check_result(
                [[i], [1, 5]], PITCH_RESULT.GROUND_OUT__DOUBLE_PLAY)
            self.check_result([[i], [1, 6]], PITCH_RESULT.STRIKE)
            self.check_result([[i], [2, 2]], PITCH_RESULT.DOUBLE__3_BASE)
            self.check_result([[i], [2, 3]], PITCH_RESULT.POP_OUT)
            self.check_result([[i], [2, 4]], PITCH_RESULT.SINGLE__2_BASE)
            self.check_result([[i], [2, 5]], PITCH_RESULT.STRIKE)
            self.check_result([[i], [2, 6]], PITCH_RESULT.GROUND_OUT)
            self.check_result([[i], [3, 3]], PITCH_RESULT.TRIPLE)
            self.check_result([[i], [3, 4]], PITCH_RESULT.STRIKE)
            self.check_result([[i], [3, 5]], PITCH_RESULT.GROUND_OUT)
            self.check_result([[i], [3, 6]], PITCH_RESULT.FLY_OUT)
            self.check_result([[i], [4, 4]], PITCH_RESULT.ERROR__1_BASE)
            self.check_result([[i], [4, 5]], PITCH_RESULT.FLY_OUT)
            self.check_result([[i], [4, 6]], PITCH_RESULT.FLY_OUT__RBI_THIRD)
            self.check_result([[i], [5, 5]], PITCH_RESULT.SINGLE__1_BASE)
            self.check_result([[i], [5, 6]], PITCH_RESULT.POP_OUT)
            self.check_result([[i], [6, 6]], PITCH_RESULT.HOME_RUN)

    def test__run_next_action__ball(self):
        for i in range(5, 7):
            self.check_result([[i]], PITCH_RESULT.BALL)
