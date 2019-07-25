from src.eggeliste_crawler import Tournament

driver_path = "C:/Users/Joppe/Documents/chromedriver/chromedriver.exe"
url = "http://www.bridgekrets.no/result/view/1755/2019-02-25?node=63169"
print(Tournament.get_all_scores(url, driver_path)[0].name1)
