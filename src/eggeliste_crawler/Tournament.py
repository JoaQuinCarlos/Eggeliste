from selenium import webdriver
import pandas as pd

from src.eggeliste_crawler.PairBoard import PairBoard
from src.eggeliste_crawler.PairScore import PairScore
from src.eggeliste_crawler.SuitEnum import Suit
from src.eggeliste_crawler.DeclearerEnum import Declearer


class Tournament:

    def __init__(self, boards, rounds, pairs, year, month, date):
        self.boards = boards
        self.rounds = rounds
        self.pairs = pairs
        self.year = year
        self.month = month
        self.date = date


def get_pair_scores(driver):
    scores = []
    expandables = driver.find_elements_by_class_name("expandable")

    for expandable in expandables:
        names = expandable.find_elements_by_class_name("name")
        numbers = expandable.find_elements_by_class_name("number")
        players = str.split(names[0].text, " - ")
        clubs = str.split(names[1].text, " - ")
        expandable.click()
        if len(clubs) == 1:
            scores.append(PairScore(players[0], players[1], clubs[0], clubs[0], numbers[0].text, numbers[1].text))

    pair_details = driver.find_elements_by_class_name("pairdetail")
    count = 0
    for pair in pair_details:
        boards = []
        board_list = pair.find_elements_by_tag_name("tr")[2:-1]
        for board in board_list:
            tds = board.find_elements_by_tag_name("td")
            names = board.find_elements_by_class_name("name")
            numbers = board.find_elements_by_class_name("numbers")
            board_number = board.find_elements_by_class_name("board-no")[0].text
            contract_level = names[0].text
            contract_suit = get_suit(names[0])
            declearer = tds[4]
            tricks = tds[5]
            lead_level = names[1].text
            lead_suit = get_suit(names[1])
            score = numbers[0]
            egge_enum = get_declearer(numbers[-4:])
            boards.append(
                PairBoard(board_number, contract_level, contract_suit, declearer, tricks, lead_level, lead_suit, score,
                          egge_enum))
        scores[count].eggeliste = boards
    return scores


def get_all_scores(url, webdriver_path):
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    scores = get_pair_scores(driver)
    return scores


def get_suit(board):
    if len(board.find_elements_by_class_name("card-c")) == 1:
        return Suit.CLUB
    elif len(board.find_elements_by_class_name("card-d")) == 1:
        return Suit.DIAMONDS
    elif len(board.find_elements_by_class_name("card-h")) == 1:
        return Suit.HEARTS
    elif len(board.find_elements_by_class_name("card-s")) == 1:
        return Suit.SPADES
    elif len(board.find_elements_by_class_name("card-n")) == 1:
        return Suit.NOTRUMP
    return None


def get_declearer(number_list):
    if len(number_list[0].text > 0):
        return Declearer.NEFORING
    elif len(number_list[1].text > 0):
        return Declearer.SWFORING
    elif len(number_list[2].text > 0):
        return Declearer.NEUTSPILL
    elif len(number_list[3].text > 0):
        return Declearer.SWUTSPILL
