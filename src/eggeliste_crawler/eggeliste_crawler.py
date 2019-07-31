from src.eggeliste_crawler.obj.Tournament import Tournament
from src.eggeliste_crawler.wrappers.TournamentWrapper import create_tournament
import time

driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
url = "http://www.bridgekrets.no/result/view/1755/2019-02-25?node=63169"
t1 = time.time()
tour = create_tournament(url, driver_path)
print(time.time() - t1)
print(tour.date)
# res = Tournament.get_all_scores(url, driver_path)
