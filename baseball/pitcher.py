#!/usr/bin/env python3

from enum import IntEnum
from typing import Dict, List

from . import random


class PITCH_RESULT(IntEnum):
    BALL = 1,
    SWING = 2,
    STRIKE = 3,
    TRIPLE = 4,
    POP_OUT = 5,
    FLY_OUT = 6,
    HOME_RUN = 7,
    GROUND_OUT = 8,
    HIT_BY_PITCH = 9,
    ERROR__1_BASE = 10,
    SINGLE__1_BASE = 11,
    SINGLE__2_BASE = 12,
    DOUBLE__2_BASE = 13,
    DOUBLE__3_BASE = 14,
    FLY_OUT__RBI_THIRD = 15,
    GROUND_OUT__DOUBLE_PLAY = 16


class Pitcher:
    __pitch_lookup: Dict[int, PITCH_RESULT] = {
        1: PITCH_RESULT.SWING,
        2: PITCH_RESULT.SWING,
        3: PITCH_RESULT.SWING,
        4: PITCH_RESULT.SWING,
        5: PITCH_RESULT.BALL,
        6: PITCH_RESULT.BALL
    }

    __swing_lookup: Dict[int, Dict[int, PITCH_RESULT]] = {
        1: {
            1: PITCH_RESULT.DOUBLE__2_BASE,
            2: PITCH_RESULT.GROUND_OUT__DOUBLE_PLAY,
            3: PITCH_RESULT.HIT_BY_PITCH,
            4: PITCH_RESULT.SINGLE__1_BASE,
            5: PITCH_RESULT.GROUND_OUT__DOUBLE_PLAY,
            6: PITCH_RESULT.STRIKE
        },
        2: {
            2: PITCH_RESULT.DOUBLE__3_BASE,
            3: PITCH_RESULT.POP_OUT,
            4: PITCH_RESULT.SINGLE__2_BASE,
            5: PITCH_RESULT.STRIKE,
            6: PITCH_RESULT.GROUND_OUT
        },
        3: {
            3: PITCH_RESULT.TRIPLE,
            4: PITCH_RESULT.STRIKE,
            5: PITCH_RESULT.GROUND_OUT,
            6: PITCH_RESULT.FLY_OUT
        },
        4: {
            4: PITCH_RESULT.ERROR__1_BASE,
            5: PITCH_RESULT.FLY_OUT,
            6: PITCH_RESULT.FLY_OUT__RBI_THIRD
        },
        5: {
            5: PITCH_RESULT.SINGLE__1_BASE,
            6: PITCH_RESULT.POP_OUT
        },
        6: {
            6: PITCH_RESULT.HOME_RUN
        }
    }

    @staticmethod
    def _validate_results(results: List[int], length: int, name: str) -> None:
        assert isinstance(results, list), 'Invalid {}: {}'.format(name, results)
        assert len(results) == length, 'Invalid {} size: {}'.format(name, results)
        for idx, val in enumerate(results):
            assert isinstance(val, int), 'Invalid {} at {}: {}'.format(name, idx, val)
            assert val >= 1 and val <= 6, 'Invalid {} at {}: {}'.format(name, idx, val)

    @staticmethod
    def run_next_action() -> None:
        pitch = random.D6s.roll()
        Pitcher._validate_results(pitch, 1, 'pitch')
        pitch_result = Pitcher.__pitch_lookup[pitch[0]]
        if pitch_result == PITCH_RESULT.BALL:
            return pitch_result
        else:
            swing = random.D6s.roll(2)
            Pitcher._validate_results(swing, 2, 'swing')
            return Pitcher.__swing_lookup[swing[0]][swing[1]]
