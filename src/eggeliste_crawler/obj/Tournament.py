from selenium import webdriver

from src.eggeliste_crawler.obj.Contract import Contract
from src.eggeliste_crawler.obj.PairBoard import PairBoard
from src.eggeliste_crawler.obj.PairScore import PairScore
from src.eggeliste_crawler.enums.SuitEnum import Suit
from src.eggeliste_crawler.enums.DeclearerEnum import Declearer


class Tournament:

    def __init__(self, title, host, boards, rounds, pairs, year, month, date, pair_stats):
        self.title = title
        self.host = host
        self.boards = boards
        self.rounds = rounds
        self.pairs = pairs
        self.year = year
        self.month = month
        self.date = date
        self.pair_stats = pair_stats

