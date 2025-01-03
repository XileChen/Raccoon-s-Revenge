"""A1: Raccoon Raiders game objects (all tasks)

CSC148, Winter 2022

This code is provided solely for the personal and private use of students
taking the CSC148 course at the University of Toronto. Copying for purposes
other than this use is expressly prohibited. All forms of distribution of this
code, whether as given or with any changes, are expressly prohibited.

Authors: Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver, and
Sophia Huynh.

All of the files in this directory and all subdirectories are:
Copyright (c) 2022 Diane Horton, Sadia Sharmin, Dina Sabie, Jonathan Calver,
and Sophia Huynh.

=== Module Description ===
This module contains all of the classes necessary for a1_game.py to run.
"""

from __future__ import annotations

import random
from random import shuffle
from typing import List, Tuple, Optional

# Each raccoon moves every this many turns
RACCOON_TURN_FREQUENCY = 20

# Directions dx, dy
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DIRECTIONS = [LEFT, UP, RIGHT, DOWN]


def get_shuffled_directions() -> List[Tuple[int, int]]:
    """
    Provided helper that returns a shuffled copy of DIRECTIONS.
    You should use this where appropriate
    """
    to_return = DIRECTIONS[:]
    shuffle(to_return)
    return to_return


class GameBoard:
    """A game board on which the game is played.

    === Public Attributes ===
    ended:
        whether this game has ended or not
    turns:
        how many turns have passed in the game
    width:
        the number of squares wide this board is
    height:
        the number of squares high this board is


    === Representation Invariants ===
    turns >= 0
    width > 0
    height > 0
    No tile in the game contains more than 1 character, except that a tile
    may contain both a Raccoon and an open GarbageCan.

    === Sample Usage ===
    See examples in individual method docstrings.

    === Private Attributes ===
    _player:
        the player of the game
    _raccoons:
        the list of raccoons in the game.
    _recycling_bins:
        the list of recycling bins in the game
    _garbage_cans:
        the list of garbage cans in the game.
    """
    ended: bool
    turns: int
    width: int
    height: int
    _player: Optional[Player]
    _raccoons: List[Raccoon]
    _recycling_bins: List[RecyclingBin]
    _garbage_cans: List[GarbageCan]

    def __init__(self, w: int, h: int) -> None:
        """Initialize this Board to be of the given width <w> and height <h> in
        squares. A board is initially empty (no characters) and no turns have
        been taken.

        >>> b = GameBoard(3, 3)
        >>> b.width == 3
        True
        >>> b.height == 3
        True
        >>> b.turns == 0
        True
        >>> b.ended
        False
        """

        self.ended = False
        self.turns = 0

        self.width = w
        self.height = h

        self._player = None
        self._raccoons = []
        self._recycling_bins = []
        self._garbage_cans = []

    def place_character(self, c: Character) -> None:
        """Record that character <c> is on this board.

        This method should only be called from Character.__init__.

        The decisions you made about new private attributes for class GameBoard
        will determine what you do here.

        Preconditions:
        - c.board == self
        - Character <c> has not already been placed on this board.
        - The tile (c.x, c.y) does not already contain a character, with the
        exception being that a Raccoon can be placed on the same tile where
        an unlocked GarbageCan is already present.

        Note: The testing will depend on this method to set up the board,
        as the Character.__init__ method calls this method.

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)  # when a Raccoon is created, it is placed on b
        >>> b.at(1, 1)[0] == r  # requires GameBoard.at be implemented to work
        True
        """
        if isinstance(c, Player):
            self._player = c
        if isinstance(c, Raccoon):
            self._raccoons.append(c)
        if isinstance(c, RecyclingBin):
            self._recycling_bins.append(c)
        if isinstance(c, GarbageCan):
            self._garbage_cans.append(c)

    def at(self, x: int, y: int) -> List[Character]:
        """Return the characters at tile (x, y).

        If there are no characters or if the (x, y) coordinates are not
        on the board, return an empty list.
        There may be as many as two characters at one tile,
        since a raccoon can climb into a garbage can.

        Note: The testing will depend on this method to allow us to
        access the Characters on your board, since we don't know how
        you have chosen to store them in your private attributes,
        so make sure it is working properly!

        >>> b = GameBoard(3, 2)
        >>> r = Raccoon(b, 1, 1)
        >>> b.at(1, 1)[0] == r
        True
        >>> p = Player(b, 0, 1)
        >>> b.at(0, 1)[0] == p
        True
        """
        lst = []
        if (self._player is not None) and self._player.x == x \
                and self._player.y == y:
            lst.append(self._player)
        for raccoon in self._raccoons:
            if raccoon.x == x and raccoon.y == y:
                lst.append(raccoon)
        for recycling_bin in self._recycling_bins:
            if recycling_bin.x == x and recycling_bin.y == y:
                lst.append(recycling_bin)
        for garbage_can in self._garbage_cans:
            if garbage_can.x == x and garbage_can.y == y:
                lst.append(garbage_can)
        return lst

    def _chr(self, tile: Tuple[int, int]) -> chr:
        """
        Return the chr at the tile

        >>> b = GameBoard(3, 2)
        >>> r = RecyclingBin(b, 1, 1)
        >>> b._chr((1, 1))
        'B'
        """
        x = tile[0]
        y = tile[1]
        grid_lst = self.at(x, y)
        if len(grid_lst) == 0:
            return '-'
        if len(grid_lst) == 1:
            ch = grid_lst[0]
            if isinstance(ch, RecyclingBin):
                return 'B'
            if isinstance(ch, Raccoon):
                if isinstance(ch, SmartRaccoon):
                    return 'S'
                else:
                    return 'R'
            if isinstance(ch, GarbageCan):
                if ch.locked is True:
                    return 'C'
                else:
                    return 'O'
            else:
                return 'P'
        else:
            return '@'

    def to_grid(self) -> List[List[chr]]:
        """
        Return the game state as a list of lists of chrs (letters) where:

        'R' = Raccoon
        'S' = SmartRaccoon
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        Each inner list represents one row of the game board.

        >>> b = GameBoard(3, 2)
        >>> _ = Player(b, 0, 0)
        >>> _ = Raccoon(b, 1, 1)
        >>> _ = GarbageCan(b, 2, 1, True)
        >>> b.to_grid()
        [['P', '-', '-'], ['-', 'R', 'C']]
        """
        outer_lst = []
        for i in range(self.height):
            inner_lst = []
            for j in range(self.width):
                tile = (j, i)
                ch = self._chr(tile)
                inner_lst.append(ch)
            outer_lst.append(inner_lst)
        return outer_lst

    def __str__(self) -> str:
        """
        Return a string representation of this board.

        The format is the same as expected by the setup_from_grid method.

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 1)
        >>> print(b)
        ---
        -R-
        >>> _ = Player(b, 0, 0)
        >>> _ = GarbageCan(b, 2, 1, False)
        >>> print(b)
        P--
        -RO
        >>> str(b)
        'P--\\n-RO'
        """
        board_lst = self.to_grid()
        board_str = ''
        for inner_lst in board_lst:
            for grid_str in inner_lst:
                board_str += grid_str
            board_str += '\n'
        board_str = board_str[:-1]
        return board_str

    def setup_from_grid(self, grid: str) -> None:
        """
        Set the state of this GameBoard to correspond to the string <grid>,
        which represents a game board using the following chars:

        'R' = Raccoon not in a GarbageCan
        'P' = Player
        'C' = closed GarbageCan
        'O' = open GarbageCan
        'B' = RecyclingBin
        '@' = Raccoon in GarbageCan
        '-' = Empty tile

        There is a newline character between each board row.

        >>> b = GameBoard(4, 4)
        >>> b.setup_from_grid('P-B-\\n-BRB\\n--BB\\n-C--')
        >>> str(b)
        'P-B-\\n-BRB\\n--BB\\n-C--'
        """
        lines = grid.split("\n")
        width = len(lines[0])
        height = len(lines)
        self.__init__(width, height)  # reset the board to an empty board
        y = 0
        for line in lines:
            x = 0
            for char in line:
                if char == 'R':
                    Raccoon(self, x, y)
                elif char == 'S':
                    SmartRaccoon(self, x, y)
                elif char == 'P':
                    Player(self, x, y)
                elif char == 'O':
                    GarbageCan(self, x, y, False)
                elif char == 'C':
                    GarbageCan(self, x, y, True)
                elif char == 'B':
                    RecyclingBin(self, x, y)
                elif char == '@':
                    GarbageCan(self, x, y, False)
                    Raccoon(self, x, y)  # always makes it a Raccoon
                    # Note: the order mattered above, as we have to place the
                    # Raccoon BEFORE the GarbageCan (see the place_character
                    # method precondition)
                x += 1
            y += 1

    # a helper method you may find useful in places
    def on_board(self, x: int, y: int) -> bool:
        """Return True iff the position x, y is within the boundaries of this
        board (based on its width and height), and False otherwise.
        """
        return 0 <= x <= self.width - 1 and 0 <= y <= self.height - 1

    def give_turns(self) -> None:
        """Give every turn-taking character one turn in the game.

        The Player should take their turn first and the number of turns
        should be incremented by one. Then each other TurnTaker
        should be given a turn if RACCOON_TURN_FREQUENCY turns have occurred
        since the last time the TurnTakers were given their turn.

        After all turns are taken, check_game_end should be called to
        determine if the game is over.

        Precondition:
        self._player is not None

        >>> b = GameBoard(4, 3)
        >>> p = Player(b, 0, 0)
        >>> r = Raccoon(b, 1, 1)
        >>> b.turns
        0
        >>> for _ in range(RACCOON_TURN_FREQUENCY - 1):
        ...     b.give_turns()
        >>> b.turns == RACCOON_TURN_FREQUENCY - 1
        True
        >>> (r.x, r.y) == (1, 1)  # Raccoon hasn't had a turn yet
        True
        >>> (p.x, p.y) == (0, 0)  # Player hasn't had any inputs
        True
        >>> p.record_event(RIGHT)
        >>> b.give_turns()
        >>> (r.x, r.y) != (1, 1)  # Raccoon has had a turn!
        True
        >>> (p.x, p.y) == (1, 0)  # Player moved right!
        True
        """
        self._player.take_turn()
        self.turns += 1  # PROVIDED, DO NOT CHANGE

        if self.turns % RACCOON_TURN_FREQUENCY == 0:  # PROVIDED, DO NOT CHANGE
            for raccoon in self._raccoons:
                raccoon.take_turn()
        self.check_game_end()  # PROVIDED, DO NOT CHANGE

    def handle_event(self, event: Tuple[int, int]) -> None:
        """Handle a user-input event.

        The board's Player records the event that happened, so that when the
        Player gets a turn, it can make the move that the user input indicated.
        """
        self._player.record_event(event)

    def check_game_end(self) -> Optional[int]:
        """Check if this game has ended. A game ends when all the raccoons on
        this game board are either inside a can or trapped.

        If the game has ended:
        - update the ended attribute to be True
        - Return the score, where the score is given by:
            (number of raccoons trapped) * 10 + the adjacent_bin_score
        If the game has not ended:
        - update the ended attribute to be False
        - return None

        >>> b = GameBoard(3, 2)
        >>> _ = Raccoon(b, 1, 0)
        >>> _ = Player(b, 0, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> b.check_game_end() is None
        True
        >>> b.ended
        False
        >>> _ = RecyclingBin(b, 2, 0)
        >>> b.check_game_end()
        11
        >>> b.ended
        True
        """
        trapped_lst = []
        all_r_trapped = False
        for r in self._raccoons:
            if r.check_trapped() and r.inside_can is False:
                trapped_lst.append(r)
        if len(trapped_lst) == len(self._raccoons):
            all_r_trapped = True

        inside_lst = []
        all_r_inside = False
        for r in self._raccoons:
            if r.inside_can:
                inside_lst.append(r)
        if len(inside_lst) == len(self._raccoons):
            all_r_inside = True

        if all_r_trapped:
            self.ended = True
            return len(self._raccoons) * 10 + self.adjacent_bin_score()
        elif all_r_inside:
            self.ended = True
            return self.adjacent_bin_score()
        else:
            return None

    def adjacent_bin_score(self) -> int:
        """
        Return the size of the largest cluster of adjacent recycling bins
        on this board.

        Two recycling bins are adjacent when they are directly beside each other
        in one of the four directions (up, down, left, right).

        See Task #5 in the handout for ideas if you aren't sure how
        to approach this problem.

        >>> b = GameBoard(3, 3)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> print(b)
        B--
        -B-
        --B
        >>> b.adjacent_bin_score()
        1
        >>> _ = RecyclingBin(b, 2, 1)
        >>> print(b)
        B--
        -BB
        --B
        >>> b.adjacent_bin_score()
        3
        >>> _ = RecyclingBin(b, 0, 1)
        >>> print(b)
        B--
        BBB
        --B
        >>> b.adjacent_bin_score()
        5
        """
        rb_left_lst = self._recycling_bins.copy()
        score_lst = []
        while len(rb_left_lst) != 0:
            rb0 = random.choice(rb_left_lst)
            dictionary = {}
            next_q = list([])
            next_q.append(rb0)
            while len(next_q) != 0:
                a = next_q.pop(0)
                dictionary[a] = self._adj(a)
                change_next_q(dictionary, a, next_q)
            adj_rb_lst = dictionary.keys()
            score = len(adj_rb_lst)
            score_lst.append(score)
            rb_left_lst = list(set(rb_left_lst) - set(adj_rb_lst))
        return max(score_lst)

    def _adj(self, rb: RecyclingBin) -> List[RecyclingBin]:
        """Return a list of all the recycling bins which are adjacent to the
        recycling bin rb on this board.

        The order of the list should correspond with the order in DIRECTIONS.

        Precondition: rb is on the board.
        >>> b = GameBoard(5, 5)
        >>> _ = RecyclingBin(b, 0, 1)
        >>> _ = RecyclingBin(b, 0, 0)
        >>> rb_l = b._adj(RecyclingBin(b, 0, 1))
        >>> char = rb_l[0]
        >>> chr_x = char.x
        >>> chr_y = char.y
        >>> b.at(chr_x, chr_y)[0] in rb_l
        True
        """
        rb_lst = []
        for direction in DIRECTIONS:
            next_x = rb.x + direction[0]
            next_y = rb.y + direction[1]
            if self.on_board(next_x, next_y):
                next_lst = self.at(next_x, next_y)
                if len(next_lst) == 1 and isinstance(next_lst[0], RecyclingBin):
                    rb_lst.append(next_lst[0])
        return rb_lst


class Character:
    """A character that has (x,y) coordinates and is associated with a given
    board.

    This class is abstract and should not be directly instantiated.

    NOTE: To reduce the amount of documentation in subclasses, we have chosen
    not to repeat information about the public attributes in each subclass.
    Remember that the attributes are not inherited, but only exist once we call
    the __init__ of the parent class.

    === Public Attributes ===
    board:
        the game board that this Character is on
    x, y:
        the coordinates of this Character on the board

    === Representation Invariants ===
    x, y are valid coordinates in board (i.e. board.on_board(x, y) is True)
    """
    board: GameBoard
    x: int
    y: int

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Character with board <b>, and
        at tile (<x>, <y>).

        When a Character is initialized, it is placed on board <b>
        by calling the board's place_character method. Refer to the
        preconditions of place_character, which must be satisfied.
        """
        self.board = b
        self.x, self.y = x, y
        self.board.place_character(self)  # this associates self with the board!

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Move this character to the tile

        (self.x + direction[0], self.y + direction[1]) if possible. Each child
        class defines its own version of what is possible.

        Return True if the move was successful and False otherwise.

        """
        raise NotImplementedError

    def get_char(self) -> chr:
        """
        Return a single character (letter) representing this Character.
        """
        raise NotImplementedError


# Note: You can safely ignore PyCharm's warning about this class
# not implementing abstract method(s) from its parent class.
class TurnTaker(Character):
    """
    A Character that can take a turn in the game.

    This class is abstract and should not be directly instantiated.
    """

    def take_turn(self) -> None:
        """
        Take a turn in the game. This method must be implemented in any subclass
        """
        raise NotImplementedError


class RecyclingBin(Character):
    """A recycling bin in the game.

    === Sample Usage ===
    >>> rb = RecyclingBin(GameBoard(4, 4), 2, 1)
    >>> rb.x, rb.y
    (2, 1)
    """

    def move(self, direction: Tuple[int, int]) -> bool:
        """Move this recycling bin to tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return whether or not this move was successful.

        If the new tile is occupied by another RecyclingBin, push
        that RecyclingBin one tile away in the same direction and take
        its tile (as described in the Assignment 1 handout).

        If the new tile is occupied by any other Character or if it
        is beyond the boundaries of the board, do nothing and return False.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> rb = RecyclingBin(b, 0, 0)
        >>> rb.move(UP)
        False
        >>> rb.move(DOWN)
        True
        >>> b.at(0, 1) == [rb]
        True
        """
        all_rb_lst = [self]
        next_x = self.x + direction[0]
        next_y = self.y + direction[1]
        next_lst = self.board.at(next_x, next_y)
        while (len(next_lst) == 1) and isinstance(next_lst[0], RecyclingBin) \
                and (self.board.on_board(next_x, next_y) is True):
            all_rb_lst.append(next_lst[0])
            next_x += direction[0]
            next_y += direction[1]
            next_lst = self.board.at(next_x, next_y)
        rb_last = all_rb_lst[-1]
        f_next_x = rb_last.x + direction[0]
        f_next_y = rb_last.y + direction[1]
        if self.board.on_board(f_next_x, f_next_y) is False:
            return False
        else:
            if len(self.board.at(f_next_x, f_next_y)) == 0 and \
                    len(all_rb_lst) == 1:
                rb_last.x = f_next_x
                rb_last.y = f_next_y
                return True
            if len(self.board.at(f_next_x, f_next_y)) == 0 and \
                    len(all_rb_lst) != 1:
                for i in range(len(all_rb_lst) - 1):
                    all_rb_lst[i].x = all_rb_lst[i + 1].x
                    all_rb_lst[i].y = all_rb_lst[i + 1].y
                rb_last.x = f_next_x
                rb_last.y = f_next_y
                return True
            else:
                return False

    def get_char(self) -> chr:
        """
        Return the character 'B' representing a RecyclingBin.
        """
        return 'B'


class Player(TurnTaker):
    """The Player of this game.

    === Sample Usage ===
    >>> b = GameBoard(3, 1)
    >>> p = Player(b, 0, 0)
    >>> p.record_event(RIGHT)
    >>> p.take_turn()
    >>> (p.x, p.y) == (1, 0)
    True
    >>> g = GarbageCan(b, 0, 0, False)
    >>> p.move(LEFT)
    True
    >>> g.locked
    True
    """
    # === Private Attributes ===
    # _last_event:
    #   The direction corresponding to the last keypress event that the user
    #   made, or None if there is currently no keypress event left to process
    _last_event: Optional[Tuple[int, int]]

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Player with board <b>,
        and at tile (<x>, <y>)."""

        TurnTaker.__init__(self, b, x, y)
        self._last_event = None

    def record_event(self, direction: Tuple[int, int]) -> None:
        """Record that <direction> is the last direction that the user
        has specified for this Player to move. Next time take_turn is called,
        this direction will be used.
        Precondition:
        direction is in DIRECTIONS
        """
        self._last_event = direction

    def take_turn(self) -> None:
        """Take a turn in the game.

        For a Player, this means responding to the last user input recorded
        by a call to record_event.
        """
        if self._last_event is not None:
            self.move(self._last_event)
            self._last_event = None

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Player to the tile:
                (self.x + direction[0], self.y + direction[1])
        if possible and return True if the move is successful.

        If the new tile is occupied by a Racooon, a locked GarbageCan, or if it
        is beyond the boundaries of the board, do nothing and return False.

        If the new tile is occupied by a movable RecyclingBin, the player moves
        the RecyclingBin and moves to the new tile.

        If the new tile is unoccupied, the player moves to that tile.

        If a Player attempts to move towards an empty, unlocked GarbageCan, the
        GarbageCan becomes locked. The player's position remains unchanged in
        this case. Also return True in this case, as the Player has performed
        the action of locking the GarbageCan.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> p = Player(b, 0, 0)
        >>> p.move(UP)
        False
        >>> p.move(DOWN)
        True
        >>> b.at(0, 1) == [p]
        True
        >>> _ = RecyclingBin(b, 1, 1)
        >>> p.move(RIGHT)
        True
        >>> b.at(1, 1) == [p]
        True
        """
        next_x = self.x + direction[0]
        next_y = self.y + direction[1]
        next_lst = self.board.at(next_x, next_y)
        if self.board.on_board(next_x, next_y) is False:
            return False
        if self.board.on_board(next_x, next_y) and len(next_lst) == 0:
            self.x = next_x
            self.y = next_y
            return True
        if self.board.on_board(next_x, next_y) and len(next_lst) == 2:
            return False
        if self.board.on_board(next_x, next_y) and len(next_lst) == 1:
            ch = next_lst[0]
            if isinstance(ch, GarbageCan):
                if ch.locked is False:
                    ch.locked = True
                    return True
                else:
                    return False
            if isinstance(ch, RecyclingBin):
                if ch.move(direction) is False:
                    return False
                else:
                    self.x = next_x
                    self.y = next_y
                    return True
            else:
                return False
        else:
            return False

    def get_char(self) -> chr:
        """
        Return the character 'P' representing this Player.
        """
        return 'P'


class Raccoon(TurnTaker):
    """A raccoon in the game.

    === Public Attributes ===
    inside_can:
        whether or not this Raccoon is inside a garbage can

    === Representation Invariants ===
    inside_can is True iff this Raccoon is on the same tile as an open
    GarbageCan.

    === Sample Usage ===
    >>> r = Raccoon(GameBoard(11, 11), 5, 10)
    >>> r.x, r.y
    (5, 10)
    >>> r.inside_can
    False
    """
    inside_can: bool

    def __init__(self, b: GameBoard, x: int, y: int) -> None:
        """Initialize this Raccoon with board <b>, and
        at tile (<x>, <y>). Initially a Raccoon is not inside
        of a GarbageCan, unless it is placed directly inside an open GarbageCan.

        >>> r = Raccoon(GameBoard(5, 5), 5, 10)
        """
        self.inside_can = False
        # since this raccoon may be placed inside an open garbage can,
        # we need to initially set the inside_can attribute
        # BEFORE calling the parent init, which is where the raccoon is actually
        # placed on the board.
        TurnTaker.__init__(self, b, x, y)

    def check_trapped(self) -> bool:
        """Return True iff this raccoon is trapped. A trapped raccoon is
        surrounded on 4 sides (diagonals don't matter) by recycling bins, other
        raccoons (including ones in garbage cans), the player, and/or board
        edges. Essentially, a raccoon is trapped when it has nowhere it could
        move.

        Reminder: A racooon cannot move diagonally.

        >>> b = GameBoard(3, 3)
        >>> r = Raccoon(b, 2, 1)
        >>> _ = Raccoon(b, 2, 2)
        >>> _ = Player(b, 2, 0)
        >>> r.check_trapped()
        False
        >>> _ = RecyclingBin(b, 1, 1)
        >>> r.check_trapped()
        True
        """
        now_lst = self.board.at(self.x, self.y)
        if len(now_lst) == 2:
            self.inside_can = True
        for direction in DIRECTIONS:
            next_x = self.x + direction[0]
            next_y = self.y + direction[1]
            next_lst = self.board.at(next_x, next_y)
            if self.board.on_board(next_x, next_y) and len(next_lst) == 0:
                return False
            if self.board.on_board(next_x, next_y) and len(next_lst) == 1:
                ch = next_lst[0]
                if isinstance(ch, GarbageCan):
                    return False
        return True

    def move(self, direction: Tuple[int, int]) -> bool:
        """Attempt to move this Raccoon in <direction> and return whether
        or not this was successful.

        If the tile one tile over in that direction is occupied by the Player,
        a RecyclingBin, or another Raccoon, OR if the tile is not within the
        boundaries of the board, do nothing and return False.

        If the tile is occupied by an unlocked GarbageCan that has no Raccoon
        in it, this Raccoon moves there and we have two characters on one tile
        (the GarbageCan and the Raccoon). If the GarbageCan is locked, this
        Raccoon uses this turn to unlock it and return True.

        If a Raccoon is inside of a GarbageCan, it will not move. Do nothing and
        return False.

        Return True if the Raccoon unlocks a GarbageCan or moves from its
        current tile.

        Precondition:
        direction in DIRECTIONS

        >>> b = GameBoard(4, 2)
        >>> r = Raccoon(b, 0, 0)
        >>> r.move(UP)
        False
        >>> r.move(DOWN)
        True
        >>> b.at(0, 1) == [r]
        True
        >>> g = GarbageCan(b, 1, 1, True)
        >>> r.move(RIGHT)
        True
        >>> r.x, r.y  # Raccoon didn't change its position
        (0, 1)
        >>> not g.locked  # Raccoon unlocked the garbage can!
        True
        >>> r.move(RIGHT)
        True
        >>> r.inside_can
        True
        >>> len(b.at(1, 1)) == 2  # Raccoon and GarbageCan are both at (1, 1)!
        True
        """
        if self.check_trapped() is False and self.inside_can is False:
            next_x = self.x + direction[0]
            next_y = self.y + direction[1]
            next_lst = self.board.at(next_x, next_y)
            if self.board.on_board(next_x, next_y) and len(next_lst) == 0:
                self.x = next_x
                self.y = next_y
                return True
            if self.board.on_board(next_x, next_y) and len(next_lst) == 1:
                ch = next_lst[0]
                if isinstance(ch, GarbageCan) and ch.locked is False:
                    self.x = next_x
                    self.y = next_y
                    self.inside_can = True
                    return True
                if isinstance(ch, GarbageCan) and ch.locked:
                    ch.locked = False
                    return True
        return False

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a Raccoon is in a GarbageCan, it stays where it is.

        Otherwise, it randomly attempts (if it is not blocked) to move in
        one of the four directions, with equal probability.

        >>> b = GameBoard(3, 4)
        >>> r1 = Raccoon(b, 0, 0)
        >>> r1.take_turn()
        >>> (r1.x, r1.y) in [(0, 1), (1, 0)]
        True
        >>> r2 = Raccoon(b, 2, 1)
        >>> _ = RecyclingBin(b, 2, 0)
        >>> _ = RecyclingBin(b, 1, 1)
        >>> _ = RecyclingBin(b, 2, 2)
        >>> r2.take_turn()  # Raccoon is trapped
        >>> r2.x, r2.y
        (2, 1)
        """
        if self.check_trapped() is False and self.inside_can is False:
            direction_lst = []
            for direction in DIRECTIONS:
                next_x = self.x + direction[0]
                next_y = self.y + direction[1]
                next_lst = self.board.at(next_x, next_y)
                if self.board.on_board(next_x, next_y) and len(next_lst) == 0:
                    direction_lst.append(direction)
                if self.board.on_board(next_x, next_y) and len(next_lst) == 1 \
                        and isinstance(next_lst[0], GarbageCan):
                    direction_lst.append(direction)
            direction = random.choice(direction_lst)
            self.move(direction)

    def get_char(self) -> chr:
        """
        Return '@' to represent that this Raccoon is inside a garbage can
        or 'R' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'R'


class SmartRaccoon(Raccoon):
    """A smart raccoon in the game.

    Behaves like a Raccoon, but when it takes a turn, it will move towards
    a GarbageCan if it can see that GarbageCan in its line of sight.
    See the take_turn method for details.

    SmartRaccoons move in the same way as Raccoons.

    === Sample Usage ===
    >>> b = GameBoard(8, 1)
    >>> s = SmartRaccoon(b, 4, 0)
    >>> s.x, s.y
    (4, 0)
    >>> s.inside_can
    False
    """

    def take_turn(self) -> None:
        """Take a turn in the game.

        If a SmartRaccoon is in a GarbageCan, it stays where it is.

        A SmartRaccoon checks along the four directions for
        the closest non-occupied GarbageCan that has nothing blocking
        it from reaching that GarbageCan (except possibly the Player).

        If there is a tie for the closest GarbageCan, a SmartRaccoon
        will prioritize the directions in the order indicated in DIRECTIONS.

        If there are no GarbageCans in its line of sight along one of the four
        directions, it moves exactly like a Raccoon. A GarbageCan is in its
        line of sight if there are no other Raccoons, RecyclingBins, or other
        GarbageCans between this SmartRaccoon and the GarbageCan. The Player
        may be between this SmartRaccoon and the GarbageCan though.

        >>> b = GameBoard(8, 2)
        >>> s = SmartRaccoon(b, 4, 0)
        >>> _ = GarbageCan(b, 3, 1, False)
        >>> _ = GarbageCan(b, 0, 0, False)
        >>> _ = GarbageCan(b, 7, 0, False)
        >>> s.take_turn()
        >>> s.x == 5
        True
        >>> s.take_turn()
        >>> s.x == 6
        True
        """
        direction_lst = []
        distance_lst = []
        for direction in DIRECTIONS:
            next_x = self.x + direction[0]
            next_y = self.y + direction[1]
            if self.board.on_board(next_x, next_y) is True:
                next_lst = self.board.at(next_x, next_y)
                num = 0
                while (len(next_lst) == 0 or isinstance(
                        next_lst[0], Player)) and (
                        self.board.on_board(next_x, next_y) is True):
                    next_x += direction[0]
                    next_y += direction[1]
                    next_lst = self.board.at(next_x, next_y)
                    num += 1
                distance = num + 1
                if len(next_lst) == 1 and \
                        isinstance(next_lst[0], GarbageCan) and \
                        next_lst[0].locked is False:
                    direction_lst.append(direction)
                    distance_lst.append(distance)
        if len(direction_lst) == 0:
            # act like regular raccoon
            Raccoon.take_turn(self)
        else:
            m = min(distance_lst)
            i = 0
            while not distance_lst[i] == m:
                i += 1
            true_direction = direction_lst[i]
            self.x += true_direction[0]
            self.y += true_direction[1]

    def get_char(self) -> chr:
        """
        Return '@' to represent that this SmartRaccoon is inside a Garbage Can
        and 'S' otherwise.
        """
        if self.inside_can:
            return '@'
        return 'S'


class GarbageCan(Character):
    """A garbage can in the game.

    === Public Attributes ===
    locked:
        whether or not this GarbageCan is locked.

    === Sample Usage ===
    >>> b = GameBoard(2, 2)
    >>> g = GarbageCan(b, 0, 0, False)
    >>> g.x, g.y
    (0, 0)
    >>> g.locked
    False
    """
    locked: bool

    def __init__(self, b: GameBoard, x: int, y: int, locked: bool) -> None:
        """Initialize this GarbageCan to be at tile (<x>, <y>) and store
        whether it is locked or not based on <locked>.
        """

        Character.__init__(self, b, x, y)
        self.locked = locked

    def get_char(self) -> chr:
        """
        Return 'C' to represent a closed garbage can and 'O' to represent
        an open garbage can.
        """
        if self.locked:
            return 'C'
        return 'O'

    def move(self, direction: Tuple[int, int]) -> bool:
        """
        Garbage cans cannot move, so always return False.
        """
        return False


# A helper function you may find useful for Task #5, depending on how
# you implement it.
def get_neighbours(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    """
    Return the coordinates of the four tiles adjacent to <tile>.

    This does NOT check if they are valid coordinates of a board.

    >>> ns = set(get_neighbours((2, 3)))
    >>> {(2, 2), (2, 4), (1, 3), (3, 3)} == ns
    True
    """
    rslt = []
    for direction in DIRECTIONS:
        rslt.append((tile[0] + direction[0], tile[1] + direction[1]))
    return rslt


def change_next_q(dictionary: dict,
                  a: RecyclingBin, next_q: list) -> None:
    """Change the list next_q.

    Precondition: a is in the dictionary.
    >>> b = GameBoard(5, 5)
    >>> a_1 = RecyclingBin(b, 1, 2)
    >>> a_2 = RecyclingBin(b, 1, 1)
    >>> dictionary_1 = {a_1: [RecyclingBin(b, 1, 1)]}
    >>> n_lst = []
    >>> change_next_q(dictionary_1, a_1, n_lst)
    >>> len(n_lst) == 1
    True
    """
    for m in dictionary[a]:
        if (m not in dictionary) and (m not in next_q):
            next_q.append(m)


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import python_ta
    python_ta.check_all(config={
        'allowed-io': [],
        'allowed-import-modules': ['doctest', 'python_ta', 'typing',
                                   'random', '__future__', 'math'],
        'disable': ['E1136'],
        'max-attributes': 15,
        'max-module-lines': 1600
    })
