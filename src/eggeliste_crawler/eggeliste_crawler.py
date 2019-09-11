from src.eggeliste_crawler.wrappers.TournamentWrapper import create_tournament
from src.eggeliste_crawler.db import *
from src.eggeliste_crawler.URL_supplier import get_links
from src.eggeliste_crawler.enums.TournamentTypeEnum import *
from src.eggeliste_crawler.statsApi import *

invalid_links = [
    "http://www.bridgekrets.no/result/view/1755/2012-08-06?node=63169",
    "http://bridgekrets.no/index.php/result/view/1745/2014-09-18?node=74510",
    "http://www.bridgekrets.no/result/view/1710/2014-12-22paaskecupen2015?node=63256",
    "http://www.bridgekrets.no/result/view/1710/2014-12-22?node=63256",
    "http://www.bridgekrets.no/result/view/1710/2016-06-18?node=63256"
]


def save_tournament_to_db(url, driver_path, conn, main_url):
    tour = create_tournament(url, driver_path)
    if(tour.type != TournamentType.TEAM):
        persist_tournament(conn, tour, main_url)


def save_all_tournaments(url, driver_path, conn):
    links = get_links(url, driver_path)
    for link in links:
        if link in invalid_links:
            print(link, "is invalid.")
        elif not is_persisted(conn, link):
            print("Saving", link, "to database.")
            save_tournament_to_db(link, driver_path, conn, url)
        else:
            print(link, "is already persisted.")


def print_all_tournaments(conn):
    tournaments = get_all_tournaments(conn)
    for tournament in tournaments:
        print(tournament)


def print_all_tournaments_by_club(conn, club):
    tournaments = get_all_tournaments_by_club(conn, club)
    for tournament in tournaments:
        print(tournament)
    print("Number of tournaments: ", len(tournaments))


def print_all_clubs(conn):
    clubs = get_all_clubs(conn)
    for club in clubs:
        print(club)


database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
conn = create_connection(database)

# get_avg_score_for_pair(conn, "Joakim Sæther", "Svein Ingar Sæther")
# get_avg_score_for_pair(conn, "Joakim Sæther", "Arnt Ola Løhre")
# get_avg_score_for_pair(conn, "Per Mælen", "Trond Stafne")
# get_avg_score_for_player(conn, "Arnfinn Helgemo")
driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
url = "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Hemne-BK/Resultater"
#
print_all_tournaments(conn)
# print_all_tournaments_by_club(conn, "Berkåk BK")
print_all_clubs(conn)
# save_all_tournaments(url, driver_path, conn)
# save_tournament_to_db("http://www.bridgekrets.no/result/view/1710/2014-05-13?node=63256", driver_path, conn, url)
conn.close()
