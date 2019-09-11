from selenium import webdriver


def get_links(url, webdriver_path):
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    links = driver.find_elements_by_tag_name("a")
    links = set([link.get_attribute("href") for link in links])
    return [str(link) for link in links if (str.startswith(str(link), "http://www.bridgekrets.no") or str.startswith(str(link), "http://bridgekrets.no")) and "result/view" in str(link)]


def main_urls():
    urls = [
        "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Melhus-BK/Resultater",
        "http://bridgekrets.no/index.php/Kretser/NBF-Soer-Troendelag/Klubber/Lundamo-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Berkaak-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Fillan-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Hemne-BK/Resultater"
    ]
    return urls
