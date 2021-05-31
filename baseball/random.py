#!/usr/bin/env python3

import random


class D6s:
    @staticmethod
    def roll(count: int = 1) -> int:
        results = []
        for _ in range(count):
            results.append(random.randint(1, 6))
        return results
