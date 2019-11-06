import math as ma
from db import create_connection


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
    print("Number of boards: ", num_boards)
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
        if r[16] == 'MP':
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


def get_doubled_stats_for_player(boards, player):
    board_count, doubled_declearer, doubled_defence, redoubled_declearer, \
    redoubled_defence, doubled_declearer_made, doubled_defence_made, \
    redoubled_declearer_made, redoubled_defence_made = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for board in boards:
        if board[16] == player or board[17] == player or player is None:  # Correct player
            board_count += 1
            if board[6] == 1:  # Doubled
                if board[13] == "NEFORING" or board[13] == "SWFORING":
                    doubled_declearer += 1
                    if board[9] >= board[4] + 6:
                        doubled_declearer_made += 1
                elif board[13] == "NEUTSPILL" or board[13] == "SWUTSPILL":
                    doubled_defence += 1
                    if board[9] >= board[4] + 6:
                        doubled_defence_made += 1
            elif board[7] == 1:
                if board[13] == "NEFORING" or board[13] == "SWFORING":
                    redoubled_declearer += 1
                    if board[9] >= board[4] + 6:
                        redoubled_declearer_made += 1
                elif board[13] == "NEUTSPILL" or board[13] == "SWUTSPILL":
                    redoubled_defence += 1
                    if board[9] >= board[4] + 6:
                        redoubled_defence_made += 1

    print(player)
    print("Total boards: ", board_count)
    print("Doubled contracts decleared: ", doubled_declearer, "(", 100 * doubled_declearer/board_count, "%)")
    if doubled_declearer > 0:
        print("Doubled contracts decleared made: ", doubled_declearer_made, "(", 100 * doubled_declearer_made/doubled_declearer, "%)")
    print("Doubled contracts defended: ", doubled_defence, "(", 100 * doubled_defence/board_count, "%)")
    if doubled_defence > 0:
        print("Doubled contracts defended made: ", doubled_defence_made, "(", 100 * doubled_defence_made/doubled_defence, "%)")
    print("Redoubled contracts decleared: ", redoubled_declearer, "(", 100 * redoubled_declearer/board_count, "%)")
    if redoubled_declearer > 0:
        print("Redoubled contracts decleared made: ", redoubled_declearer_made, "(", 100 * redoubled_declearer_made/redoubled_declearer, "%)")
    print("Redoubled contracts defended: ", redoubled_defence, "(", 100 * redoubled_defence/board_count, "%)")
    if redoubled_defence > 0:
        print("Redoubled contracts defended made: ", redoubled_defence_made, "(", 100 * redoubled_defence_made/redoubled_defence, "%)")


def get_doubled_stats_for_pair(boards, player1, player2):
    board_count, doubled_declearer, doubled_defence, redoubled_declearer, \
    redoubled_defence, doubled_declearer_made, doubled_defence_made, \
    redoubled_declearer_made, redoubled_defence_made = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for board in boards:
        if (board[16] == player1 or board[16] == player2) and (board[17] == player1 or board[17] == player2):  # Correct pair
            board_count += 1
            if board[6] == 1:  # Doubled
                if board[13] == "NEFORING" or board[13] == "SWFORING":
                    doubled_declearer += 1
                    if board[9] >= board[4] + 6:
                        doubled_declearer_made += 1
                elif board[13] == "NEUTSPILL" or board[13] == "SWUTSPILL":
                    doubled_defence += 1
                    if board[9] >= board[4] + 6:
                        doubled_defence_made += 1
            elif board[7] == 1:
                if board[13] == "NEFORING" or board[13] == "SWFORING":
                    redoubled_declearer += 1
                    if board[9] >= board[4] + 6:
                        redoubled_declearer_made += 1
                elif board[13] == "NEUTSPILL" or board[13] == "SWUTSPILL":
                    redoubled_defence += 1
                    if board[9] >= board[4] + 6:
                        redoubled_defence_made += 1

    print("Pair: ", player1, "-", player2)
    print("Total boards: ", board_count)
    print("Doubled contracts decleared: ", doubled_declearer, "(", 100 * doubled_declearer/board_count, "%)")
    if doubled_declearer > 0:
        print("Doubled contracts decleared made: ", doubled_declearer_made, "(", 100 * doubled_declearer_made/doubled_declearer, "%)")
    print("Doubled contracts defended: ", doubled_defence, "(", 100 * doubled_defence/board_count, "%)")
    if doubled_defence > 0:
        print("Doubled contracts defended made: ", doubled_defence_made, "(", 100 * doubled_defence_made/doubled_defence, "%)")
    print("Redoubled contracts decleared: ", redoubled_declearer, "(", 100 * redoubled_declearer/board_count, "%)")
    if redoubled_declearer > 0:
        print("Redoubled contracts decleared made: ", redoubled_declearer_made, "(", 100 * redoubled_declearer_made/redoubled_declearer, "%)")
    print("Redoubled contracts defended: ", redoubled_defence, "(", 100 * redoubled_defence/board_count, "%)")
    if redoubled_defence > 0:
        print("Redoubled contracts defended made: ", redoubled_defence_made, "(", 100 * redoubled_defence_made/redoubled_defence, "%)")


def get_pair_against_pair(boards, player1, player2, opponent1, opponent2):
    board_count, score = 0, 0
    for board in boards:
        if (((board[2] == opponent1 or board[3] == opponent1) and (board[2] == opponent2 or board[3] == opponent2)) and (board[16] == player1 or board[17] == player1) and (board[16] == player2 or board[17] == player2)):
            board_count += 1
            score += score_to_percent(board[12], board[30])
    print("Score for", player1, "-", player2, "against", opponent1 , "-", opponent2)
    print("Number of boards: ", board_count)
    if board_count > 0:
        print("Average score: ", score / board_count)


def get_player_against_player(boards, player1, player2):
    board_count, score = 0, 0
    for board in boards:
        if (board[2] == player2 or board[3] == player2) and (board[16] == player1 or board[17] == player2):
            board_count += 1
            score += score_to_percent(board[12], board[30])
    print("Score for", player1, "against", player2)
    print("Number of boards:", board_count)
    if board_count > 0:
        print("Average score:", score / board_count)


def get_all_tournaments(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM tournament")
    return c.fetchall()


def get_all_clubs(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM club")
    return c.fetchall()


def score_to_percent(score, pairs):
    top = ma.floor((pairs - 2) / 2) * 2
    score = (top / 2) + score
    return 100 * (score / top)
