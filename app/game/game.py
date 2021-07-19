import random
import datetime

from app.game.constants import GameStatus


class Player:
    """
    Represents user and its moves on the board.
    """

    def __init__(self, moves, is_computer):
        self.moves = moves
        self.is_computer = is_computer

    @property
    def raw_moves(self):
        return {c["coords"] for c in self.moves}

    @property
    def max_points_in_seq(self):
        """
        Get the length of the longest line that user currently has.
        This is used further as the indicatation of whether
        user has won or not by comparing with the number needed
        to win a game.
        """
        # TODO improve this method
        moves_count = len(self.raw_moves)
        g_max = moves_count if moves_count <= 1 else 0
        if len(self.raw_moves) >= 2:
            max_x = max(m[0] for m in self.raw_moves)
            min_x = min(m[0] for m in self.raw_moves)
            max_y = max(m[1] for m in self.raw_moves)
            min_y = min(m[1] for m in self.raw_moves)
            for m in self.raw_moves:
                hor_points = {(i, m[1]) for i in range(min_x, max_x + 1)}
                vertical_points = {(m[0], i) for i in range(min_y, max_y + 1)}
                diagonal_1_points = {
                    (m[0] + i, m[1] + i) for i, _ in enumerate(range(m[0], max_x + 1))
                }.union(
                    {(m[0] - i, m[1] - i) for i, _ in enumerate(range(min_y, m[1] + 1))}
                )
                diagonal_2_points = {
                    (m[0] - i, m[1] + i) for i, _ in enumerate(range(min_x, m[0] + 1))
                }.union(
                    {(m[0] + i, m[1] - i) for i, _ in enumerate(range(m[0], max_x + 1))}
                )
                iterables = (
                    hor_points,
                    vertical_points,
                    diagonal_1_points,
                    diagonal_2_points,
                )
                for i in iterables:
                    l_max = 0
                    for point in i:
                        if point in self.raw_moves:
                            l_max += 1
                        else:
                            l_max = 0
                        if l_max > g_max:
                            g_max = l_max
        return g_max

    def add_move(self, move, order):
        self.moves.append(
            {
                "coords": move,
                "order": order,
            }
        )


class Board:
    """
    Encapsulates methods that are used to interact with the board.
    """

    def __init__(self, size, user_moves, computer_moves):
        self.size = size
        self.user_player = Player(user_moves, is_computer=False)
        self.computer_player = Player(computer_moves, is_computer=True)

    @property
    def cells(self):
        return {(x, y) for x in range(0, self.size) for y in range(0, self.size)}

    @property
    def free_cells(self):
        return self.cells - self.user_player.raw_moves - self.computer_player.raw_moves

    @property
    def number_of_moves(self):
        return len(self.user_player.moves) + len(self.computer_player.moves)

    def get_player(self, is_computer=False):
        return [
            player
            for player in [self.user_player, self.computer_player]
            if player.is_computer == is_computer
        ][0]

    def add_move(self, move, computer=False):
        obj = self.get_player(is_computer=computer)
        return obj.add_move(move, order=self.number_of_moves + 1)

    def has_won(self, line_len_to_win, computer=False):
        obj = self.get_player(is_computer=computer)
        return obj.max_points_in_seq >= line_len_to_win


class Game:
    """
    Main class that represents game and with which client
    should interact.
    Contains methods to communicate with mongo db game records (from_mongo, data_for_mongo)
    as well as reference to Board object which is used to as a delegate object
    to do some calculations.
    """

    def __init__(
        self, board_size, user_moves, computer_moves, line_len_to_win, status, **kwargs
    ):
        self.board = Board(board_size, user_moves, computer_moves)
        self.line_len_to_win = line_len_to_win

    @classmethod
    def from_mongo(cls, mongo_obj):
        """
        Initializer to get instance from mondo db object.
        """
        from app.game.serializers import GameSchema

        schema = GameSchema()
        data = schema.dump(mongo_obj)
        return cls(**data)

    @property
    def data_for_mongo(self):
        """
        Data that should be inserted to mongo upon next game round.
        """
        status = self.status
        data = {
            "user_moves": self.board.user_player.moves,
            "computer_moves": self.board.computer_player.moves,
            "status": status,
        }
        if not status == GameStatus.IN_PROGRESS:
            data["completed_at"] = datetime.datetime.now()
        return data

    @property
    def status(self):
        if not self.free_cells:
            return GameStatus.TIE
        elif self.has_won(computer=False):
            return GameStatus.USER_WIN
        elif self.has_won(computer=True):
            return GameStatus.COMPUTER_WIN
        return GameStatus.IN_PROGRESS

    @property
    def free_cells(self):
        return self.board.free_cells

    def make_move(self, move, computer=False):
        self.board.add_move(move=move, computer=computer)

    def calculate_move(self):
        """
        Calculate a move for computer merely by selecting among free cells on a board.
        """
        # TODO improve the algorithm used to calculate the best move for the computer
        assert self.free_cells, "There are no free cells on a board."
        return random.choice(tuple(self.free_cells))

    def has_won(self, computer=False):
        return self.board.has_won(self.line_len_to_win, computer=computer)
