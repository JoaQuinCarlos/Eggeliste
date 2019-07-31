from selenium import webdriver
import time

from src.eggeliste_crawler.enums.DeclearerEnum import Declearer
from src.eggeliste_crawler.enums.SuitEnum import Suit
from src.eggeliste_crawler.enums.TournamentTypeEnum import TournamentType
from src.eggeliste_crawler.obj.Contract import Contract
from src.eggeliste_crawler.obj.PairBoard import PairBoard
from src.eggeliste_crawler.obj.PairScore import PairScore
from src.eggeliste_crawler.obj.Tournament import Tournament


def create_tournament(url, webdriver_path):
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    metadata = driver.find_elements_by_class_name("metainfo")[0]
    title = get_title(driver)
    host = get_host(metadata)
    boards, rounds, pairs = get_boards_rounds_pairs(metadata)
    year, month, date = get_year_month_date(metadata)
    tournament_type = get_tournament_type(driver.find_elements_by_tag_name("tbody")[0])
    pair_stats = get_pair_scores(driver, tournament_type)

    return Tournament(url=url, type=tournament_type, title=title, host=host, boards=boards, rounds=rounds, pairs=pairs, year=year,
                      month=month, date=date, pair_stats=pair_stats)


def get_title(driver):
    return str(driver.find_elements_by_tag_name("h1")[0].get_attribute("innerText"))


def get_host(metadata):
    return str(metadata.find_elements_by_tag_name("div")[2].get_attribute("innerText")).replace("Arrangør: ", "")


def get_boards_rounds_pairs(metadata):
    innerText = str(metadata.find_elements_by_tag_name("div")[3].get_attribute("innerText"))
    numbers = [int(s) for s in innerText.replace(",", " ").replace(":", " ").split() if s.isdigit()]
    return numbers[0], numbers[1], numbers[2]


def get_year_month_date(metadata):
    innerText = str(metadata.find_elements_by_tag_name("div")[1].get_attribute("innerText"))
    numbers = [int(s) for s in innerText.replace(": ", "-").split("-") if s.isdigit()]
    return numbers[0], numbers[1], numbers[2]


def get_tournament_type(table):
    headers = table.find_elements_by_class_name("score-total")
    headers = headers[0].find_elements_by_tag_name("th")
    if len(headers) == 6:
        return TournamentType.MP
    else:
        return TournamentType.IMP_ACROSS


def get_pair_scores(driver, tournament_type):
    scores = []
    expandables = driver.find_elements_by_class_name("expandable")

    for expandable in expandables:
        names = expandable.find_elements_by_class_name("name")
        numbers = expandable.find_elements_by_class_name("number")
        players = str.split(names[0].text, " - ")
        clubs = str.split(names[1].text, " - ")
        expandable.click()
        score = float(str(numbers[0].get_attribute("innerText")).replace(",", "."))
        if tournament_type == TournamentType.MP:
            percent = float(str(numbers[1].get_attribute("innerText")).replace(",", "."))
        else:
            percent = None
        if len(clubs) == 1:
            scores.append(PairScore(players[0], players[1], clubs[0], clubs[0], score, percent))
        else:
            scores.append(PairScore(players[0], players[1], clubs[0], clubs[1], score, percent))

    pair_details = driver.find_elements_by_class_name("pairdetail")
    count = 0
    for pair in pair_details:
        boards = []
        board_list = pair.find_elements_by_tag_name("tr")[2:-1]
        t1 = time.time()
        for board in board_list:
            t2 = time.time()
            boards.append(get_board(board))
            print("Time for board: ", time.time() - t2)
        scores[count].eggeliste = boards
        print("Time for method: ", time.time() - t1)
        count += 1
    return scores


def get_board(board):
    tds = board.find_elements_by_tag_name("td")
    names = board.find_elements_by_class_name("name")
    numbers = board.find_elements_by_class_name("number")

    board_number = int(board.find_elements_by_class_name("board-no")[0].get_attribute("data-boardno"))
    contract = get_contract(names[0])
    declearer = tds[4].get_attribute("innerText")
    score = float(str(numbers[1].get_attribute("innerText")).replace(",", "."))
    if contract.contract_level is None:
        return PairBoard(board_number, contract, declearer, 0, 0, None, score, Declearer.SITOUT)
    lead_level = get_card_value(names[1])
    lead_suit = get_suit(names[1])

    tricks = int(tds[5].get_attribute("innerText"))
    egge_enum = get_declearer(numbers[-4:])
    return PairBoard(board_number, contract, declearer, tricks, lead_level, lead_suit, score,
                     egge_enum)


def get_all_scores(url, webdriver_path):
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    scores = get_pair_scores(driver)
    return scores


def get_contract(contractElement):
    contract_suit = get_suit(contractElement)
    innerText = str(contractElement.get_attribute("innerText"))
    doubled = False
    redoubled = False
    if '-' in innerText:
        return Contract(None, None, None, None)
    if 'Pass' in innerText:
        return Contract(0, None, doubled, redoubled)
    if 'XX' in innerText:
        redoubled = True
        innerText = innerText[0]
    elif 'X' in innerText:
        doubled = True
        innerText = innerText[0]
    contract_level = [int(s) for s in innerText.split() if s.isdigit()][0]
    return Contract(contract_level, contract_suit, doubled, redoubled)


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
    return None  # Passed out


def get_card_value(card):
    lead_level = str(card.get_attribute("innerText")).replace(" ", "").replace("\n", "")
    if lead_level in '12456789':
        return int(lead_level)
    elif lead_level == 'T':
        return 10
    elif lead_level == 'J':
        return 11
    elif lead_level == 'Q':
        return 12
    elif lead_level == 'K':
        return 13
    elif lead_level == 'A':
        return 14
    return 0  # Passed out


def get_declearer(number_list):
    declearerStr1 = str(number_list[0].get_attribute("innerText"))
    declearerStr2 = str(number_list[1].get_attribute("innerText"))
    declearerStr3 = str(number_list[2].get_attribute("innerText"))
    declearerStr4 = str(number_list[3].get_attribute("innerText"))

    if len(declearerStr1) > 0:
        return Declearer.NEFORING
    elif len(declearerStr2) > 0:
        return Declearer.SWFORING
    elif len(declearerStr3) > 0:
        return Declearer.NEUTSPILL
    elif len(declearerStr4) > 0:
        return Declearer.SWUTSPILL
    else:
        return Declearer.ALLPASS
