import requests
from bs4 import BeautifulSoup


# TODO: Eggeliste
def get_player_list(url, ignore=[], klubbnr=1755):
    url = url
    src = requests.get(url)
    plain_text = src.text
    soup = BeautifulSoup(plain_text, features="html.parser")  # Get html-code from result overview
    cnt = 0
    processed = 0
    playerlist = {}
    scorelist = {}
    for link in soup.findAll('a'):  # For each tournament in the overview
        if cnt % 2 == 0:  # Only the tournament title (avoiding the link-dates)
            skip = False
            for string in ignore:
                if string in str(link):
                    skip = True
            if str.startswith(str(link), '<a href="/result/view/' + str(klubbnr)) and not skip:  # Only the tournament links, and avoiding the ignored strings.
                href = "http://www.bridgekrets.no" + link.get('href')
                print(link.get('href'))
                resultat_side = requests.get(href)
                resultat_side_plain_text = resultat_side.text
                resultat_soup = BeautifulSoup(resultat_side_plain_text, features="html.parser")  # Get html-code for a tournament

                pairs, boards = 0, 0

                # Retrieve number of boards and number of pairs
                for div in resultat_soup.findAll('div'):
                    if str.startswith(str(div), '<div>Spill: '):
                        boards = get_boards(div)
                        pairs = get_paris(div)

                name_class = resultat_soup.findAll('td', {'class': 'name'})
                score_class = resultat_soup.findAll('td', {'class': 'number'})

                # Club name also has class 'name'. Only picking every second appearance.
                for i in range(0, pairs * 2):
                    if i % 2 == 0:
                        score = str(score_class[i + 1]).replace(',', '.', 1)
                        if is_number(score[-10:-5].replace(".", "")):
                            playerlist = add_played_to_dict(str(name_class[i]), playerlist, boards)
                            scorelist = add_played_to_dict(str(name_class[i]), scorelist, boards * float(score[-10:-5]))
                processed += 1
                print("Processed:", processed)
        cnt += 1

    rank = 1
    c = {}
    for k, v in playerlist.items():
        c[k] = scorelist[k] / v

    player_arr = sorted(((v, k) for k, v in playerlist.items()), reverse=True)
    score_arr = sorted(((v, k) for k, v in c.items()), reverse=True)

    for v, k in player_arr:
        print("Rank:", rank, "%s: %d" % (k, v))
        rank += 1

    rank = 1
    for v, k in score_arr:
        if playerlist[k] > 1000:
            print("%d: %s: %f %d" % (rank, k, v, playerlist[k]))
            rank += 1


def add_played_to_dict(names, playerlist, value=1.0):
    names = names[17:-5]
    names_arr = names.split(sep=" - ")
    if len(names_arr) == 2:
        name1, name2 = names_arr[0], names_arr[1]
        if name1 in playerlist:
            playerlist[name1] += value
        else:
            playerlist[name1] = value
        if name2 in playerlist:
            playerlist[name2] += value
        else:
            playerlist[name2] = value

    if len(names_arr) == 1:
        if names_arr[0] in playerlist:
            playerlist[names_arr[0]] += value
        else:
            playerlist[names_arr[0]] = value
    return playerlist


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

# Melhus
link = "http://www.bridgekrets.no/Kretser/NBF-Soer-Troendelag/Klubber/Melhus-BK/Resultater"
get_player_list(link, ["km", "2015-02-16", "2014-02-10"])

# Heimdal
# link = "http://www.bridgekrets.no/Kretser/NBF-Midt-Troendelag/Klubber/Heimdal-BK/Resultater"
# get_player_list(url=link, ignore=["lag", "IMP", "bedrift", "vrmesterskapet2013-omgang1"], klubbnr=1833)

# Lundamo
# link = "http://bridgekrets.no/index.php/Kretser/NBF-Soer-Troendelag/Klubber/Lundamo-BK/Resultater"
# get_player_list(url=link, ignore=["lag", "jubileum"], klubbnr=1745)

# Berkåk
# link = "http://bridgekrets.no/index.php/Kretser/NBF-Soer-Troendelag/Klubber/Berkaak-BK/Resultater"
# get_player_list(url=link, ignore=["lag", "Gauldal", "gauldal"], klubbnr=1710)


# Vesterålen
# link = "http://www.bridgekrets.no/Kretser/NBF-Lofoten-og-Vesteraalen/Klubber/Vestvaagoey-BK/Resultater"
# get_player_list(url=link, ignore=['open', 'Open', 'kmlag', 'jubileum', 'divisjon', 'butler', 'lag', 'test', '2011-12-06'], klubbnr=2285)
