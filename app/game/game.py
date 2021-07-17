class Board:
    pass


class Game:
    def __init__(self, user, user_moves, computer_moves, line_len_to_win, status, **kwargs):
        self.user = user
        self.user_moves = user_moves
        self.computer_moves = computer_moves 
        self.line_len_to_win = line_len_to_win
        self.status = status


    @classmethod
    def from_mongo(cls, mongo_obj):
        from app.game.serializers import GameSchema
        schema = GameSchema()
        data = schema.dump(mongo_obj)
        return cls(**data)
    
    @property
    def data_for_mongo(self):
        raise NotImplemented
    
    def get_free_cells(self):
        raise NotImplemented
    
    def make_move(self):
        raise NotImplemented
    
    def calculate_move(self):
        raise NotImplemented
    
    def has_wone(self):
        raise NotImplemented

