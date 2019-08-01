from src.eggeliste_crawler.obj.Tournament import Tournament
from src.eggeliste_crawler.wrappers.TournamentWrapper import create_tournament
from src.eggeliste_crawler.URL_supplier import get_links
import time

driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
url = "http://www.bridgekrets.no/result/view/1755/finalebronsefinalekmlag-1-1-525336575?node=63169"
t1 = time.time()
tour = create_tournament(url, driver_path)

print(tour.type)

# links = get_links("http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Melhus-BK/Resultater", driver_path)
#
# for link in links:
#     print(link)
