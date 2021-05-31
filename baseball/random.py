#!/usr/bin/env python3

import random


class D6s:
    @staticmethod
    def roll_one():
        return random.randint(1, 6)

    @staticmethod
    def roll_two():
        return D6s.roll_one() + D6s.roll_two()
