import math as ma


def get_avg_score_for_pair(conn, name1, name2):
    c = conn.cursor()
    c.execute("SELECT * FROM pair_score p "
              "JOIN tournament t "
              "ON p.tournament_id = t.id "
              "WHERE player_name1 IN (?, ?) "
              "AND player_name2 IN (?, ?) "
              "AND tournament_type = 'MP'", (name1, name2, name2, name1))
    res = c.fetchall()
    tot = 0
    num_boards = 0
    for r in res:
        num_boards += r[14]
        tot += r[14] * r[6]
    print("Numbaer of boards: ", num_boards)
    print("Average score: ", tot / num_boards)


def get_avg_score_for_player(conn, name1):
    c = conn.cursor()
    c.execute("SELECT * FROM pair_score p "
              "JOIN tournament t "
              "ON p.tournament_id = t.id "
              "WHERE player_name1 IN (?) "
              "OR player_name2 IN (?) "
              "AND tournament_type = 'MP'", (name1, name1))
    res = c.fetchall()
    tot = 0
    num_boards = 0
    for r in res:
        num_boards += r[14]
        tot += r[14] * r[6]
    print("Number of boards: ", num_boards)
    print("Average score: ", tot / num_boards)


def get_eggeliste_for_pair(conn, name1, name2):
    c = conn.cursor()
    c.execute("SELECT * FROM pair_board pb "
              "JOIN pair_score ps "
              "ON pb.pair_score_id = ps.id "
              "JOIN tournament t "
              "ON ps.tournament_id = t.id "
              "WHERE player_name1 IN (?, ?) "
              "AND player_name2 IN (?, ?) "
              "AND tournament_type = 'MP'", (name1, name2, name1, name2))
    res = c.fetchall()
    ne_foring = 0
    ne_foring_score = 0
    ne_mot = 0
    ne_mot_score = 0
    sw_foring = 0
    sw_foring_score = 0
    sw_mot = 0
    sw_mot_score = 0
    total_boards = 0
    for r in res:
        total_boards += 1
        if r[13] == "NEFORING":
            ne_foring += 1
            ne_foring_score += score_to_percent(r[12], r[30])
        elif r[13] == "NEUTSPILL":
            ne_mot += 1
            ne_mot_score += score_to_percent(r[12], r[30])
        elif r[13] == "SWFORING":
            sw_foring += 1
            sw_foring_score += score_to_percent(r[12], r[30])
        elif r[13] == "SWUTSPILL":
            sw_mot += 1
            sw_mot_score += score_to_percent(r[12], r[30])
    print("Total boards:", total_boards)
    print("NE føring:", (ne_foring_score / ne_foring))
    print("NE motspill:", (ne_mot_score / ne_mot))
    print("SW føring:", (sw_foring_score / sw_foring))
    print("SW motspill:", (sw_mot_score / sw_mot))


def score_to_percent(score, pairs):
    top = ma.floor((pairs - 2) / 2) * 2
    score = (top / 2) + score
    return 100 * (score / top)

