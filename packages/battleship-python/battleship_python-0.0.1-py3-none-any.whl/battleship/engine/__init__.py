#
# This file is part of the battleship-python project
#
# Copyright (c) 2024 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

"""Absolute minimalistic game engine core"""

from .util import points_from_lines


class Ship:
    def __init__(self, top_left=(0, 0), rotation=0):
        self.translation = top_left
        self.rotation = rotation  # clockwise
        self.floating_points = set(self.points)

    def __bool__(self):
        return not self.sunk

    @property
    def text_lines(self):
        return self.TEXT[self.rotation]

    @property
    def points(self):
        return points_from_lines(self.text_lines, self.translation)

    def receive_fire(self, point):
        try:
            self.floating_points.remove(point)
        except KeyError:
            return False
        return True

    @property
    def sunk(self):
        return not bool(self.floating_points)


def line_text(n):
    v, h = n * ("x",), (n * "x",)
    return {0: v, 90: h, 180: v, 270: h}


class Carrier(Ship):
    TEXT = {
        0: ("xxx", " x ", " x "),
        90: ("  x", "xxx", "  x"),
        180: (" x ", " x ", "xxx"),
        270: ("x  ", "xxx", "x  "),
    }


class Battleship(Ship):
    TEXT = line_text(4)


class Cruiser(Ship):
    TEXT = line_text(3)


class Destroyer(Ship):
    TEXT = line_text(2)


class Submarine(Ship):
    TEXT = line_text(1)


class Board:
    DEFAULT_SIZE = (10, 10)

    def __init__(self, ships, size=DEFAULT_SIZE):
        self.size = size
        self.ships = ships

    def __bool__(self):
        return any(self.ships)

    def receive_fire(self, at):
        for ship in self.ships:
            if ship.receive_fire(at):
                return ship


class Player:
    def __init__(self, name):
        self.name = name


class Game:
    """Base game with no checks"""

    def __init__(self, player1, board1, player2, board2):
        self.player1 = player1
        self.player2 = player2
        self.board1 = board1
        self.board2 = board2
        self.player = player1

    def __bool__(self):
        return all((self.board1, self.board2))

    def player_board(self, player):
        return self.board1 if player is self.player1 else self.board2

    def fire(self, at_player, at):
        board = self.player_board(at_player)
        ship = board.receive_fire(at)
        return ship, board

    def turn(self, fire_at):
        adversary = self.adversary()
        ship, board = self.fire(adversary, fire_at)
        winner = None if ship is None or board else self.player
        self.player = adversary
        return ship, winner

    def adversary(self, player=None):
        if player is None:
            player = self.player
        return self.player2 if player is self.player1 else self.player1


class BattleshipError(Exception):
    pass


class UnknownPlayer(BattleshipError):
    pass


class Engine:
    def __init__(self):
        self.players = {}

    def register_player(self, player_id, name):
        if (existing := self.get_player(player_id)) is not None:
            raise BattleshipError(f"cannot change {existing.name!r} name")
        player = Player(name)
        player.id = player_id
        self.players[player_id] = player, None
        return player

    def _get_raw_player(self, player_id):
        return self.players.get(player_id, (None, None))

    def get_player(self, player_id):
        return self._get_raw_player(player_id)[0]

    def get_player_game(self, player_id):
        return self._get_raw_player(player_id)[1]

    def get_game(self, game_id):
        for _, game in self.players.values():
            if id(game) == game_id:
                return game

    def create_ships(self):
        return [
            Carrier((0, 0)),
            Battleship((5, 0)),
            Cruiser((7, 0)),
            Destroyer((9, 0)),
            Submarine((0, 4)),
            Submarine((2, 4)),
        ]

    def create_board(self):
        return Board(ships=self.create_ships())

    def new_game(self, player_id):
        player, game = self._get_raw_player(player_id)
        if player is None:
            raise UnknownPlayer("unknown player")
        if game is not None:
            raise BattleshipError(f"{player.name!r} already in game")

        board1 = self.create_board()
        board2 = self.create_board()
        game = Game(player, board1, None, board2)
        self.players[player_id] = player, game
        return game

    def leave_game(self, player_id):
        # notify other player
        # delete game
        # update both player states to initialized
        player, game = self._get_raw_player(player_id)
        if player is None:
            raise UnknownPlayer("unknown player")
        if game is None:
            return player, game
        self.players[player.id] = player, None
        if adversary := game.adversary(player):
            self.players[adversary.id] = adversary, None
        return player, game

    def quit(self, player_id):
        self.leave_game(player_id)
        return self.players.pop(
            player_id,
        )

    def find_empty_game(self):
        for _, game in self.players.values():
            if game is not None and game.player2 is None:
                return game

    def join_game(self, player_id, game_id=None):
        # get game from ID
        # check game is waiting for 2nd player
        # add player to game
        # update game state to "running"
        # send other player notification that 2nd player joined the game
        # send player 1 notification that it can fire
        player, game = self._get_raw_player(player_id)
        if player is None:
            raise UnknownPlayer("unknown player")
        if game is not None:
            raise BattleshipError(f"{player.name!r} already in game")
        if game_id is None:
            if (game := self.find_empty_game()) is None:
                raise BattleshipError("cannot find empty game")
        else:
            game = self.get_game(game_id)
        if game is None:
            raise BattleshipError(f"unknown game ID {game_id!r}")
        if game.player2:
            raise BattleshipError("game already started")
        game.player2 = player
        self.players[player_id] = player, game
        return player, game

    def list_games(self):
        return list({id(game) for _, game in self.players.values() if game})

    def fire(self, player_id, at):
        # check player state is in game
        # check game is in "running" state
        # check it's the player turn to fire
        # fire, update game state
        # notify both players the fire result
        # switch players and notify new player that it can fire
        player, game = self._get_raw_player(player_id)
        if player is None:
            raise UnknownPlayer("unknown player")
        if game is None:
            raise BattleshipError("player not in game")
        adversary = game.adversary(player)
        if adversary is None:
            raise BattleshipError("need a 2nd player to join the game")
        if game.player != player:
            raise BattleshipError("not your turn!")
        at = tuple(at)
        ship, winner = game.turn(at)
        if winner:
            self.players[player_id] = player, None
            self.players[adversary.id] = adversary, None
        return game, winner, player, adversary, ship
