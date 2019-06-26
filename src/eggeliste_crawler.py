import requests
from bs4 import BeautifulSoup


def crawl(player1, player2, target, url):
    resultat_side = requests.get(url)
    resultat_side_plain_text = resultat_side.text
    resultat_soup = BeautifulSoup(resultat_side_plain_text, features="html.parser")  # Get html-code for a tournament

    pairs, boards, plassering = 0, 0, 0

    # Retrieve number of boards and number of pairs
    for div in resultat_soup.findAll('div'):
        if str.startswith(str(div), '<div>Spill: '):
            boards = get_boards(div)
            pairs = get_paris(div)

    name_class = resultat_soup.findAll('td', {'class': 'name'})
    eggelister = resultat_soup.findAll('tr', {'class': 'pairdetail hide'})

    for i in range(0, pairs * 2):
        if player1 in str(name_class[i]) and player2 in str(name_class[i]):
            plassering = int((i+2)/2)
            print(plassering)
    # for eggeliste in eggelister:
    #     print(eggeliste)
    print(eggelister[3])
    print(eggelister[3].findChildren()[0])
    # print(eggelister[3].findChildren()[0].findChildren()[0])


def get_boards(div):
    if is_number(str(div)[12:14]):
        return int(str(div)[12:14])
    if is_number(str(div)[12:13]):
        return int(str(div)[12:13])
    return int(str(div)[12:12])


def get_paris(div):
    if is_number(str(div)[-9:-6]):
        return int(str(div)[-9:-6])
    if is_number(str(div)[-8:-6]):
        return int(str(div)[-8:-6])
    return int(str(div)[-7:-7])


def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


crawl(player1='Arnt Ola Løhre', player2='Joakim Sæther', target='../res/test_list.csv', url='http://www.bridgekrets.no/result/view/1755/2019-02-25?node=63169')
