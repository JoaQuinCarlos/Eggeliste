from selenium import webdriver


def get_links(url, webdriver_path):
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    links = driver.find_elements_by_tag_name("a")
    links = set([link.get_attribute("href") for link in links])
    return [str(link) for link in links if str.startswith(str(link), "http://www.bridgekrets.no/result/view")]
