import sqlite3
# from src.eggeliste_crawler.db import *
#
# database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
# conn = create_connection(database)
#
# c = conn.cursor()
# c.execute("SELECT t.id "
#           "FROM tournament t "
#           "join pair_score ps "
#           "on t.id = ps.tournament_id "
#           "join pair_board pb "
#           "on ps.id = pb.pair_score_id "
#           "join club c "
#           "on t.club_id = c.id "
#           "where ps.points >  t.boards * (t.pairs / 2)"
#           "and t.tournament_type = 'MP'")

# res = set(c.fetchall())

# c.execute("delete from table pair_board")
# res = [t[0] for t in res]
# pair_scores = []
# for tournament_id in res:
#     c.execute("SELECT id "
#               "from pair_score "
#               "where tournament_id = ?", (tournament_id,))
#     r = c.fetchall()
#     for pair_score in r:
#         pair_scores.append(pair_score[0])
#
# pair_boards = []
# for pair_score_id in pair_scores:
#     c.execute("SELECT id "
#               "from pair_board "
#               "where pair_score_id = ?", (pair_score_id,))
#     r = c.fetchall()
#     for pair_board in r:
#         pair_boards.append(pair_board[0])
#
# for pair_board in pair_boards:
#     print(pair_board)
#
# print("Length: ", len(pair_boards))
# print("Len2: ", len(pair_scores))
# print("Len_tourn: ", len(res))
#
# for pair_board in pair_boards:
#     c.execute("DELETE from pair_board "
#               "WHERE id = ?", (pair_board,))
#     print("Deleted", pair_board, "from pair_boards")
#
# for pair_score in pair_scores:
#     c.execute("DELETE from pair_score "
#               "WHERE id = ?", (pair_score,))
#     print("Deleted", pair_score, "from pair_scores")

# for tournament in res:
#     c.execute("DELETE from tournament "
#               "WHERE id = ?", (tournament,))
#     print("Deleted", tournament, "from tournaments")

