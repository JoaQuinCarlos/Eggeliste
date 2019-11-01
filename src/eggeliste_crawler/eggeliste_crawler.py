from src.eggeliste_crawler.wrappers.TournamentWrapper import create_tournament
from src.eggeliste_crawler.db import *
from src.eggeliste_crawler.URL_supplier import *
from src.eggeliste_crawler.enums.TournamentTypeEnum import *
from src.eggeliste_crawler.statsApi import *

invalid_links = [
    "http://www.bridgekrets.no/result/view/1755/2012-08-06?node=63169",
    "http://bridgekrets.no/index.php/result/view/1745/2014-09-18?node=74510",
    "http://www.bridgekrets.no/result/view/1710/2014-12-22paaskecupen2015?node=63256",
    "http://www.bridgekrets.no/result/view/1710/2014-12-22?node=63256",
    "http://www.bridgekrets.no/result/view/1710/2016-06-18?node=63256",
    "http://www.bridgekrets.no/result/view/1606/2018-01-16?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2017-10-03?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2018-02-13?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2017-12-12?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2016-12-13?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2019-04-02?node=87097",
    "http://www.bridgekrets.no/result/view/1628/2016-10-17?node=63027",
    "http://www.bridgekrets.no/result/view/1606/2018-12-11?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2019-04-30?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2017-05-16?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2018-03-06?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2018-03-20?node=87097",
    "http://www.bridgekrets.no/result/view/1606/2019-04-09?node=87097",
    "http://www.bridgekrets.no/result/view/1652/2017-03-02?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2017-02-23?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2017-05-04?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2019-05-23?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2019-05-15?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2017-03-23?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2019-05-27?node=91471",
    "http://www.bridgekrets.no/result/view/1652/2017-03-09?node=91471",
    "http://www.bridgekrets.no/result/view/1650/2015-01-13?node=60452"
]


def save_tournament_to_db(url, driver_path, conn, main_url):
    tour = create_tournament(url, driver_path)
    if tour is not None:
        if tour.type != TournamentType.TEAM:
            persist_tournament(conn, tour, main_url)


def save_all_tournaments(url, driver_path, conn):
    main_links = main_urls()
    for main_url in main_links:
        links = get_links(main_url, driver_path)
        i = 0
        for link in links:
            if link in invalid_links:
                print(link, "is invalid.")
            elif not is_persisted(conn, link):
                print("Saving", link, "to database.")
                save_tournament_to_db(link, driver_path, conn, main_url)
            else:
                print(link, "is already persisted.")
            i += 1
            print("Saved", i, "tournaments out of", len(links), "for current club")


def print_all_tournaments(conn, club=None, scoring=None):
    tournaments = get_tournaments(conn, club=club, scoring=scoring)
    for tournament in tournaments:
        print(tournament)
    print("Total number of tournaments: ", len(tournaments))


def print_all_clubs(conn):
    clubs = get_all_clubs(conn)
    for club in clubs:
        print(club)
    print("Total number of clubs: ", len(clubs))


def print_all_boards(conn, club=None, player1=None, player2=None):
    boards = get_pair_boards(conn, club, player1, player2)
    for board in boards:
        print(board)
    print("Total number of boards: ", len(boards))


database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
conn = create_connection(database)

# boards = get_pair_boards(conn, player1="Arnt Ola Løhre")
#
# d = dict()
# for board in boards:
#     if board[16] in d:
#         d[board[16]] += 1
#     else:
#         d[board[16]] = 1
#     if board[17] in d:
#         d[board[17]] += 1
#     else:
#         d[board[17]] = 1
#
# for player in d:
#     print("Makker", player, "\nAntall spill: ", d[player])

driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
url = "http://bridgekrets.no/index.php/Kretser/NBF-Soer-Troendelag/Klubber/Orkdal-BK/Resultater"
# print_all_boards(conn, player1="Arnt Ola Løhre")

# print_all_tournaments(conn)
# print_all_clubs(conn)
save_all_tournaments(url, driver_path, conn)
# save_tournament_to_db("http://www.bridgekrets.no/result/view/1611/2019-03-18?node=114703", driver_path, conn, url)
conn.close()
