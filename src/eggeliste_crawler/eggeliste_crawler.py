from src.eggeliste_crawler.wrappers.TournamentWrapper import create_tournament
from src.eggeliste_crawler.db import persist_tournament
from src.eggeliste_crawler.db import *
import time


def save_tournament_to_db(url):
    driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
    database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
    tour = create_tournament(url, driver_path)
    persist_tournament(tour, database, "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Melhus-BK/Resultater")

t1 = time.time()
url = "http://www.bridgekrets.no/result/view/1755/2019-08-05?node=63169"
database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
# save_tournament_to_db(url)
print(time.time() - t1)

# res = get_all_pair_boards(database)
res = get_all_pair_boards_for_pairs(database, ["Joakim Sæther", "Svein Ingar Sæther"])

for row in res:
    print(row)
