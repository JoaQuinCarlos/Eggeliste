from selenium import webdriver


def get_links(url, webdriver_path):
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    links = driver.find_elements_by_tag_name("a")
    links = set([link.get_attribute("href") for link in links])
    return [str(link) for link in links if (str.startswith(str(link), "http://www.bridgekrets.no") or str.startswith(str(link), "http://bridgekrets.no")) and "result/view" in str(link)]


def main_urls():
    urls = [
        # "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Melhus-BK/Resultater",
        # "http://bridgekrets.no/index.php/Kretser/NBF-Soer-Troendelag/Klubber/Lundamo-BK/Resultater",
        # "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Berkaak-BK/Resultater",
        # "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Fillan-BK/Resultater",
        # "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Hemne-BK/Resultater",
        # "http://bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Oppdal-BK/Resultater",
        # "http://bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Orkdal-BK/Resultater",
        # "http://bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Singsaas-BK/Resultater",
        # "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Aukra-BK/Resul"
        # "tater",
        # "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Averoey-BK/Resultater",
        # "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/BK-Grand/Resultater2",
        # "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Fosnavaag-BK/Resultater",
        # "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Haramsoey-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Molde-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Moestknektene/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Raumaknektene-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Stranda-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Sunndalsoera-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Ulstein-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Vartdal-BK/Resultater",
        "http://www.bridgekrets.no/Kretser/NBF-Moere-og-Romsdal/Klubber/Vestnes-BK/Resultater"
    ]
    return urls
