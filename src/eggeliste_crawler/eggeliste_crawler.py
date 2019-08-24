from src.eggeliste_crawler.wrappers.TournamentWrapper import create_tournament
from src.eggeliste_crawler.db import *
from src.eggeliste_crawler.URL_supplier import get_links
from src.eggeliste_crawler.enums.TournamentTypeEnum import *
from src.eggeliste_crawler.statsApi import *


def save_tournament_to_db(url, driver_path, conn, main_url):
    tour = create_tournament(url, driver_path)
    if(tour.type != TournamentType.TEAM):
        persist_tournament(conn, tour, main_url)


def save_all_tournaments(url, driver_path, conn):
    links = get_links(url, driver_path)
    for link in links:
        if not is_persisted(conn, link):
            print("Saving", link, "to database.")
            save_tournament_to_db(link, driver_path, conn, url)
        else:
            print(link, "is already persisted.")


def print_all_tournaments(conn):
    tournaments = get_all_tournaments(conn)
    for tournament in tournaments:
        print(tournament)


def print_all_clubs(conn):
    clubs = get_all_clubs(conn)
    for club in clubs:
        print(club)


database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
conn = create_connection(database)

get_avg_score_for_pair(conn, "Joakim Sæther", "Svein Ingar Sæther")
# get_avg_score_for_pair(conn, "Joakim Sæther", "Arnt Ola Løhre")
# get_avg_score_for_pair(conn, "Per Mælen", "Trond Stafne")
# get_avg_score_for_player(conn, "Ludvig Kristoffersen")
# get_eggeliste_for_pair(conn, "Joakim Sæther", "Arnt Ola Løhre")
get_eggeliste_for_pair(conn, "Joakim Sæther", "Svein Ingar Sæther")
# driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
# url = "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Melhus-BK/Resultater"
#
# print_all_tournaments(conn)
# print_all_clubs(conn)
# save_all_tournaments(url, driver_path, conn)
# save_tournament_to_db("http://www.bridgekrets.no/result/view/1755/2013-11-18?node=63169", driver_path, conn, url)
conn.close()
