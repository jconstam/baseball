#!/usr/bin/env python3

from enum import IntEnum
from typing import Tuple

from .pitcher import PITCH_RESULT


class PlayerLocation(IntEnum):
    BENCH = 1,
    ON_DECK = 2,
    AT_BAT = 3,
    FIRST_BASE = 4,
    SECOND_BASE = 5,
    THIRD_BASE = 6,
    HOME = 7


class Player():
    def __init__(self) -> None:
        self.__location = PlayerLocation.BENCH
        self.__at_bats = 0
        self.__hit_count = 0
        self.__run_count = 0
        self.__walk_count = 0
        self.__strike_out_count = 0
        self.__field_out_count = 0

    def __check_player_is_in_field(self, message):
        assert self.__location not in [PlayerLocation.BENCH, PlayerLocation.ON_DECK], message

    def location(self) -> PlayerLocation:
        return self.__location

    def bring_on_deck(self) -> None:
        assert self.__location == PlayerLocation.BENCH, 'Cannot bring a player on deck that isn\'t on the bench'
        self.__location = PlayerLocation.ON_DECK

    def bring_up_to_bat(self) -> None:
        assert self.__location == PlayerLocation.ON_DECK, 'Cannot bring a player up to bat that isn\'t on deck'
        self.__location = PlayerLocation.AT_BAT
        self.__at_bats += 1

    def advance_bases(self, count: int) -> None:
        assert count > 0, 'Cannot advance 0 bases'
        assert count <= 4, 'Cannot advance more than 4 bases'
        self.__check_player_is_in_field('Cannot advance to the next base when not on the field')
        if self.__location + count >= PlayerLocation.HOME:
            self.__location = PlayerLocation.HOME
        else:
            self.__location += count

    def run(self) -> None:
        assert self.__location == PlayerLocation.HOME, 'Cannot score a run if the player isn\'t at home'
        self.__location = PlayerLocation.BENCH
        self.__run_count += 1

    def walk(self) -> None:
        assert self.__location == PlayerLocation.AT_BAT, 'Cannot be walked if the player isn\'t at bat'
        self.__walk_count += 1

    def hit(self) -> None:
        assert self.__location == PlayerLocation.AT_BAT, 'Cannot have a hit if the player isn\'t at bat'
        self.__hit_count += 1

    def is_out(self) -> None:
        self.__check_player_is_in_field('Cannot be out when not on the field')
        if self.__location == PlayerLocation.AT_BAT:
            self.__strike_out_count += 1
        else:
            self.__field_out_count += 1
        self.__location = PlayerLocation.BENCH
