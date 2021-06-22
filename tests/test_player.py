#!/usr/bin/env python3

import unittest

from baseball.player import Player, PlayerLocation


class PlayerExceptionTests(unittest.TestCase):
    def validate_exception_with_message(self, exception, message, function, *args, **kwargs):
        try:
            function(*args, **kwargs)
            self.fail()
        except Exception as ex:
            self.assertIsInstance(ex, exception)
            self.assertEqual(ex.args[0], message)

    def test__bring_on_deck__not_on_bench(self):
        test_player = Player()
        for i in PlayerLocation:
            if i != PlayerLocation.BENCH:
                test_player._Player__location = i
                self.validate_exception_with_message(
                    AssertionError, 'Cannot bring a player on deck that isn\'t on the bench', test_player.bring_on_deck)

    def test__bring_up_to_bat__not_on_deck(self):
        test_player = Player()
        for i in PlayerLocation:
            if i != PlayerLocation.ON_DECK:
                test_player._Player__location = i
                self.validate_exception_with_message(
                    AssertionError, 'Cannot bring a player up to bat that isn\'t on deck', test_player.bring_up_to_bat)

    def test__advance_bases__zero_bases(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.AT_BAT
        self.validate_exception_with_message(
            AssertionError, 'Cannot advance 0 bases', test_player.advance_bases, count=0)

    def test__advance_bases__five_bases(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.AT_BAT
        self.validate_exception_with_message(
            AssertionError, 'Cannot advance more than 4 bases', test_player.advance_bases, count=5)

    def test__advance_bases__not_in_field(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.BENCH
        self.validate_exception_with_message(
            AssertionError, 'Cannot advance to the next base when not on the field', test_player.advance_bases, count=1)
        test_player._Player__location = PlayerLocation.ON_DECK
        self.validate_exception_with_message(
            AssertionError, 'Cannot advance to the next base when not on the field', test_player.advance_bases, count=1)

    def test__walk__not_in_field(self):
        test_player = Player()
        for i in PlayerLocation:
            if i != PlayerLocation.AT_BAT:
                test_player._Player__location = i
                self.validate_exception_with_message(
                    AssertionError, 'Cannot be walked if the player isn\'t at bat', test_player.walk)

    def test__hit__not_in_field(self):
        test_player = Player()
        for i in PlayerLocation:
            if i != PlayerLocation.AT_BAT:
                test_player._Player__location = i
                self.validate_exception_with_message(
                    AssertionError, 'Cannot have a hit if the player isn\'t at bat', test_player.hit)

    def test__is_out__not_in_field(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.BENCH
        self.validate_exception_with_message(
            AssertionError, 'Cannot be out when not on the field', test_player.is_out)
        test_player._Player__location = PlayerLocation.ON_DECK
        self.validate_exception_with_message(
            AssertionError, 'Cannot be out when not on the field', test_player.is_out)

    def test__run__not_at_home(self):
        test_player = Player()
        for i in PlayerLocation:
            if i != PlayerLocation.HOME:
                test_player._Player__location = i
                self.validate_exception_with_message(
                    AssertionError, 'Cannot score a run if the player isn\'t at home', test_player.run)


class PlayerTests(unittest.TestCase):
    def test__constructor(self):
        test_player = Player()
        assert test_player.location() == PlayerLocation.BENCH
        assert test_player._Player__at_bats == 0
        assert test_player._Player__hit_count == 0
        assert test_player._Player__run_count == 0
        assert test_player._Player__walk_count == 0
        assert test_player._Player__strike_out_count == 0
        assert test_player._Player__field_out_count == 0

    def test__bring_on_deck(self):
        test_player = Player()
        test_player.bring_on_deck()
        assert test_player.location() == PlayerLocation.ON_DECK

    def test__bring_up_to_bat(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.ON_DECK
        test_player.bring_up_to_bat()
        assert test_player.location() == PlayerLocation.AT_BAT
        assert test_player._Player__at_bats == 1

    def test__advance_bases__at_bat(self):
        end_locations = [PlayerLocation.FIRST_BASE, PlayerLocation.SECOND_BASE, PlayerLocation.THIRD_BASE, PlayerLocation.HOME]
        for index, end_loc in enumerate(end_locations):
            test_player = Player()
            test_player._Player__location = PlayerLocation.AT_BAT
            test_player.advance_bases(index + 1)
            assert test_player.location() == end_loc

    def test__advance_bases__first_base(self):
        end_locations = [PlayerLocation.SECOND_BASE, PlayerLocation.THIRD_BASE, PlayerLocation.HOME, PlayerLocation.HOME]
        for index, end_loc in enumerate(end_locations):
            test_player = Player()
            test_player._Player__location = PlayerLocation.FIRST_BASE
            test_player.advance_bases(index + 1)
            assert test_player.location() == end_loc

    def test__advance_bases__second_base(self):
        end_locations = [PlayerLocation.THIRD_BASE, PlayerLocation.HOME, PlayerLocation.HOME, PlayerLocation.HOME]
        for index, end_loc in enumerate(end_locations):
            test_player = Player()
            test_player._Player__location = PlayerLocation.SECOND_BASE
            test_player.advance_bases(index + 1)
            assert test_player.location() == end_loc

    def test__advance_bases__third_base(self):
        end_locations = [PlayerLocation.HOME, PlayerLocation.HOME, PlayerLocation.HOME, PlayerLocation.HOME]
        for index, end_loc in enumerate(end_locations):
            test_player = Player()
            test_player._Player__location = PlayerLocation.THIRD_BASE
            test_player.advance_bases(index + 1)
            assert test_player.location() == end_loc

    def test__advance_bases__home(self):
        end_locations = [PlayerLocation.HOME, PlayerLocation.HOME, PlayerLocation.HOME, PlayerLocation.HOME]
        for index, end_loc in enumerate(end_locations):
            test_player = Player()
            test_player._Player__location = PlayerLocation.HOME
            test_player.advance_bases(index + 1)
            assert test_player.location() == end_loc

    def test__run(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.HOME
        test_player.run()
        assert test_player.location() == PlayerLocation.BENCH
        assert test_player._Player__run_count == 1

    def test__walk(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.AT_BAT
        test_player.walk()
        assert test_player._Player__walk_count == 1

    def test__hit(self):
        test_player = Player()
        test_player._Player__location = PlayerLocation.AT_BAT
        test_player.hit()
        assert test_player._Player__hit_count == 1

    def test__out(self):
        start_locations = [PlayerLocation.AT_BAT, PlayerLocation.FIRST_BASE, PlayerLocation.SECOND_BASE, PlayerLocation.THIRD_BASE]
        for start_loc in start_locations:
            test_player = Player()
            test_player._Player__location = start_loc
            test_player.is_out()
            if start_loc == PlayerLocation.AT_BAT:
                assert test_player._Player__strike_out_count == 1
            else:
                assert test_player._Player__field_out_count == 1
            assert test_player.location() == PlayerLocation.BENCH
