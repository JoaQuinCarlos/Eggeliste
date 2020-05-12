import math as ma
from src.eggeliste_crawler.db import create_connection
from src.server.DataObjects import PlayerStat


def get_player_stats(name, scoring='MP'):
    name = str.replace(name, "_", " ")

    database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
    conn = create_connection(database)
    c = conn.cursor()

    c.execute("SELECT * FROM pair_board pb "
              "JOIN pair_score ps "
              "ON pb.pair_score_id = ps.id "
              "JOIN tournament t "
              "ON ps.tournament_id = t.id "
              "WHERE player_name1 IN (?) "
              "OR player_name2 IN (?) "
              "AND tournament_type IN (?)", (name, name, scoring))

    res = c.fetchall()
    if len(res) == 0:
        return PlayerStat.PlayerStat(player_name=name, avg_score=50.0, num_boards=0, declarances=50)

    tot = 0
    dec = 0
    mot = 0
    for r in res:
        tot += r[21]
        if r[13] == 'NEFORING' or r[13] == 'SWFORING':
            dec += 1
        elif r[13] == 'NEUTSPILL' or r[13] == 'SWUTSPILL':
            mot += 1
    avg_score = tot/len(res)
    declarances = 100 * (dec / (dec + mot))

    return PlayerStat.PlayerStat(player_name=name, avg_score=avg_score, num_boards=len(res), declarances=declarances)
