from src.eggeliste_crawler.Tournament import Tournament

driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
url = "http://www.bridgekrets.no/result/view/1755/2019-02-25?node=63169"
tour = Tournament(url, driver_path)
print(tour.date)
# res = Tournament.get_all_scores(url, driver_path)
