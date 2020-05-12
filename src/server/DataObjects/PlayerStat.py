import json


class PlayerStat:

    def __init__(self, player_name, avg_score, num_boards, declarances):
        self.player_name = player_name
        self.avg_score = avg_score
        self.num_boards = num_boards
        self.declarances_in_percent = declarances


    def to_json(self):
        return json.dumps(self.__dict__)
