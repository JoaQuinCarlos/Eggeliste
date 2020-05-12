import math as ma
import operator

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
    print("Doubled contracts decleared: ", doubled_declearer, "(", 100 * doubled_declearer / board_count, "%)")
    if doubled_declearer > 0:
        print("Doubled contracts decleared made: ", doubled_declearer_made, "(",
              100 * doubled_declearer_made / doubled_declearer, "%)")
    print("Doubled contracts defended: ", doubled_defence, "(", 100 * doubled_defence / board_count, "%)")
    if doubled_defence > 0:
        print("Doubled contracts defended made: ", doubled_defence_made, "(",
              100 * doubled_defence_made / doubled_defence, "%)")
    print("Redoubled contracts decleared: ", redoubled_declearer, "(", 100 * redoubled_declearer / board_count, "%)")
    if redoubled_declearer > 0:
        print("Redoubled contracts decleared made: ", redoubled_declearer_made, "(",
              100 * redoubled_declearer_made / redoubled_declearer, "%)")
    print("Redoubled contracts defended: ", redoubled_defence, "(", 100 * redoubled_defence / board_count, "%)")
    if redoubled_defence > 0:
        print("Redoubled contracts defended made: ", redoubled_defence_made, "(",
              100 * redoubled_defence_made / redoubled_defence, "%)")


def get_doubled_stats_for_pair(boards, player1, player2):
    board_count, doubled_declearer, doubled_defence, redoubled_declearer, \
    redoubled_defence, doubled_declearer_made, doubled_defence_made, \
    redoubled_declearer_made, redoubled_defence_made = 0, 0, 0, 0, 0, 0, 0, 0, 0
    for board in boards:
        if (board[16] == player1 or board[16] == player2) and (
                board[17] == player1 or board[17] == player2):  # Correct pair
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
    print("Doubled contracts decleared: ", doubled_declearer, "(", 100 * doubled_declearer / board_count, "%)")
    if doubled_declearer > 0:
        print("Doubled contracts decleared made: ", doubled_declearer_made, "(",
              100 * doubled_declearer_made / doubled_declearer, "%)")
    print("Doubled contracts defended: ", doubled_defence, "(", 100 * doubled_defence / board_count, "%)")
    if doubled_defence > 0:
        print("Doubled contracts defended made: ", doubled_defence_made, "(",
              100 * doubled_defence_made / doubled_defence, "%)")
    print("Redoubled contracts decleared: ", redoubled_declearer, "(", 100 * redoubled_declearer / board_count, "%)")
    if redoubled_declearer > 0:
        print("Redoubled contracts decleared made: ", redoubled_declearer_made, "(",
              100 * redoubled_declearer_made / redoubled_declearer, "%)")
    print("Redoubled contracts defended: ", redoubled_defence, "(", 100 * redoubled_defence / board_count, "%)")
    if redoubled_defence > 0:
        print("Redoubled contracts defended made: ", redoubled_defence_made, "(",
              100 * redoubled_defence_made / redoubled_defence, "%)")


def get_pair_against_pair(boards, player1, player2, opponent1, opponent2):
    board_count, score = 0, 0
    for board in boards:
        if (((board[2] == opponent1 or board[3] == opponent1) and (
                board[2] == opponent2 or board[3] == opponent2)) and (
                board[16] == player1 or board[17] == player1) and (board[16] == player2 or board[17] == player2)):
            board_count += 1
            score += score_to_percent(board[12], board[30])
    print("Score for", player1, "-", player2, "against", opponent1, "-", opponent2)
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


'''
Getting the down stats for the following person(s):
- A player if only the player1-argument is given.
- A pair if both the player1-argument and the player2-argument is given.
- All players in the database if no parameters are supplied.
- A list of players if only the player_list-parameter is supplied.

The result is printed to the console as a list which is sorted 
increasingly on the average number of downs per board decleared.
'''


def get_down_stats(boards, player1=None, player2=None, player_list=None):
    board_count, number_of_downs = 0, 0
    if player1 is not None and player2 is None:
        for board in boards:
            if (board[16] == player1 or board[17] == player1) and (board[13] == 'NEFORING' or board[13] == 'SWFORING'):
                board_count += 1
                number_of_downs += number_of_down(board)
        print("Average downs per board for", player1, ":", number_of_downs / board_count)
    elif player1 is not None and player2 is not None:
        for board in boards:
            if (board[16] == player1 or board[17] == player1) and (board[16] == player2 or board[17] == player2) and (
                    board[13] == 'NEFORING' or board[13] == 'SWFORING'):
                board_count += 1
                number_of_downs += number_of_down(board)
        print("Average downs per board for", player1, "-", player2, ":", number_of_downs / board_count)
    elif player1 is None and player2 is None:
        player_dict = {}
        for board in boards:
            downs = number_of_down(board)
            if board[13] == 'NEFORING' or board[13] == 'SWFORING':
                if board[16] in player_dict:
                    player_dict[board[16]][0] += 1
                    player_dict[board[16]][1] += downs
                else:
                    player_dict[board[16]] = [1, downs]
                if board[17] in player_dict:
                    player_dict[board[17]][0] += 1
                    player_dict[board[17]][1] += downs
                else:
                    player_dict[board[17]] = [1, downs]
        reworked_dict = {}
        for player in player_dict:
            if player_dict[player][1] > 100:
                reworked_dict[player] = player_dict[player][1] / player_dict[player][0]
        reworked_dict = sorted(reworked_dict, key=reworked_dict.get)
        i = 0
        if player_list is None:
            for player in reworked_dict:
                i += 1
                print(i, ")", player, "Average number of downs:", player_dict[player][1] / player_dict[player][0])
        else:
            for player in reworked_dict:
                if player in player_list:
                    i += 1
                    print(i, ")", player, "Average number of downs:",
                          player_dict[player][1] / player_dict[player][0])


'''
Getting the slam stats for the following person(s):
- A player if only the player1-argument is given.
- A pair if both the player1-argument and the player2-argument is given.
- All players in the database if no parameters are supplied. (Implementation not complete)
- A list of players if only the player_list-parameter is supplied. (Implementation not complete)
'''
def get_slam_stats(boards, player1=None, player2=None, player_list=None):
    small_slam_fail, small_slam_made, board_count, grand_fail, grand_made = 0, 0, 0, 0, 0
    if player1 is not None and player2 is None:
        for board in boards:
            if board[16] == player1 or board[17] == player1:
                board_count += 1
                if board[13] == 'NEFORING' or board[13] == 'SWFORING':
                    if int(board[4]) == 6:
                        if number_of_down(board) > 0:
                            small_slam_fail += 1
                        else:
                            small_slam_made += 1
                    elif int(board[4]) == 7:
                        if number_of_down(board) > 0:
                            grand_fail += 1
                        else:
                            grand_made += 1
        print("Slam statistics for", player1 + ":")
        print("Percentage of small slams:", 100 * (small_slam_made + small_slam_fail) / board_count, "%")
        print("Percentage of grand slams:", 100 * (grand_made + grand_fail) / board_count, "%")
        print("Small slams made:", 100 * small_slam_made / (small_slam_fail + small_slam_made), "%", "(", small_slam_made + small_slam_fail, "small slams in total)")
        print("Grands made:", 100 * grand_made / (grand_fail + grand_made), "%", "(", grand_made + grand_fail, "grands in total)")

    if player1 is not None and player2 is not None:
        for board in boards:
            if (board[16] == player1 or board[17] == player1) and (board[16] == player2 or board[17] == player2):
                board_count += 1
                if board[13] == 'NEFORING' or board[13] == 'SWFORING':
                    if int(board[4]) == 6:
                        if number_of_down(board) > 0:
                            small_slam_fail += 1
                        else:
                            small_slam_made += 1
                    elif int(board[4]) == 7:
                        if number_of_down(board) > 0:
                            grand_fail += 1
                        else:
                            grand_made += 1
        print("Slam statistics for", player1, "-", player2 + ":")
        print("Percentage of small slams:", 100 * (small_slam_made + small_slam_fail) / board_count, "%")
        print("Percentage of grand slams:", 100 * (grand_made + grand_fail) / board_count, "%")
        print("Small slams made:", 100 * small_slam_made / (small_slam_fail + small_slam_made), "%", "(", small_slam_made + small_slam_fail, "small slams in total)")
        print("Grands made:", 100 * grand_made / (grand_fail + grand_made), "%", "(", grand_made + grand_fail, "grands in total)")

    elif player1 is None and player2 is None:
        raise NotImplementedError("This functionality is not fully implemented yet.")
        player_dict = {}
        for board in boards:
            small_fail = int(board[4]) == 6 and number_of_down(board) > 0
            small_made = int(board[4]) == 6 and number_of_down(board) == 0
            grand_fail_bool = int(board[4]) == 7 and number_of_down(board) > 0
            grand_made_bool = int(board[4]) == 7 and number_of_down(board) == 0
            if board[13] == 'NEFORING' or board[13] == 'SWFORING':
                if board[16] in player_dict:
                    player_dict[board[16]][2] += 1
                    if small_fail:
                        player_dict[board[16]][0] += 1
                    elif small_made:
                        player_dict[board[16]][1] += 1
                    elif grand_fail_bool:
                        player_dict[board[16]][3] += 1
                    elif grand_made_bool:
                        player_dict[board[16]][4] += 1
                else:
                    player_dict[board[16]] = [0, 0, 1, 0, 0]
                    if small_fail:
                        player_dict[board[16]][0] += 1
                    elif small_made:
                        player_dict[board[16]][1] += 1
                    elif grand_fail_bool:
                        player_dict[board[16]][3] += 1
                    elif grand_made_bool:
                        player_dict[board[16]][4] += 1
                if board[17] in player_dict:
                    player_dict[board[17]][2] += 1
                    if small_fail:
                        player_dict[board[17]][0] += 1
                    elif small_made:
                        player_dict[board[17]][1] += 1
                    elif grand_fail_bool:
                        player_dict[board[17]][3] += 1
                    elif grand_made_bool:
                        player_dict[board[17]][4] += 1
                else:
                    player_dict[board[17]] = [0, 0, 1, 0, 0]
                    if small_fail:
                        player_dict[board[17]][0] += 1
                    elif small_made:
                        player_dict[board[17]][1] += 1
                    elif grand_fail_bool:
                        player_dict[board[17]][3] += 1
                    elif grand_made_bool:
                        player_dict[board[17]][4] += 1



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


def number_of_down(board):
    contract_level = int(board[4])
    num_tricks = int(board[9])
    num_downs = contract_level + 6 - num_tricks
    if num_downs > 0:
        return num_downs
    return 0
