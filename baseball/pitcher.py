#!/usr/bin/env python3

from enum import IntEnum
from typing import Dict

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
        0: PITCH_RESULT.SWING,
        1: PITCH_RESULT.SWING,
        2: PITCH_RESULT.SWING,
        3: PITCH_RESULT.SWING,
        4: PITCH_RESULT.BALL,
        5: PITCH_RESULT.BALL
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
    def run_next_action():
        pitch = random.D6s.roll()
        assert pitch >= 1 and pitch <= 6, 'Invalid pitch: {}'.format(pitch)
        pitch_result = Pitcher.__pitch_lookup[pitch]
        if pitch_result == PITCH_RESULT.BALL:
            return pitch_result
        else:
            swing = random.D6s.roll(2)
            assert len(swing) == 2, 'Invalid swing size: {}'.format(swing)
            assert swing[0] >= 1 and swing[0] <= 6, 'Invalid swing[0]: {}'.format(swing[0])
            assert swing[1] >= 1 and swing[1] <= 6, 'Invalid swing[1]: {}'.format(swing[1])
            return Pitcher.__swing_lookup[swing[0]][swing[1]]
