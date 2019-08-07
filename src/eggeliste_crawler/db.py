import sqlite3
from sqlite3 import Error
from src.eggeliste_crawler.enums.TournamentTypeEnum import TournamentType


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def is_persisted(conn, url):
    c = conn.cursor()
    c.execute("SELECT * FROM tournament WHERE url = (?)", (url,))
    return len(c.fetchall()) > 0


def persist_tournament(conn, tour, host_url):
    c = conn.cursor()
    c.execute("SELECT * FROM club WHERE url = (?)", (host_url,))
    clubs = c.fetchall()
    if len(clubs) == 0:
        c.execute("INSERT INTO club(name, url) VALUES (?,?)", (tour.host, host_url))
        club_id = c.lastrowid
    else:
        club_id = clubs[0][0]
    persist_tournament_obj(tour, c, club_id)
    conn.commit()


def persist_tournament_obj(tour, c, club_id):
    date = str(tour.date) + "-" + str(tour.month) + "-" + str(tour.year)
    c.execute(
        "INSERT INTO tournament(club_id, title, url, date, rounds, boards, pairs, tournament_type) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (club_id, tour.title, tour.url, date, tour.rounds, tour.boards, tour.pairs, tour.type.name))
    tournament_id = c.lastrowid
    if tour.type != TournamentType.SINGLE:
        for pair_stat in tour.pair_stats:
            persist_pair_stat(pair_stat, c, tournament_id)


def persist_pair_stat(pair_stat, c, tournament_id):
    c.execute(
        "INSERT INTO pair_score(player_name1, player_name2, club_name1, club_name2, points, score, tournament_id) "
        "VALUES(?, ?, ?, ?, ?, ?, ?)",
        (pair_stat.name1, pair_stat.name2, pair_stat.club1, pair_stat.club2, pair_stat.points, pair_stat.score,
         tournament_id))
    pair_stat_id = c.lastrowid
    for board in pair_stat.eggeliste:
        persist_pair_board(board, c, pair_stat_id)


def persist_pair_board(board, c, pair_stat_id):
    c.execute(
        "INSERT INTO pair_board(board_number, opponent_name1, opponent_name2, contract_level, contract_suit, "
        "doubled, redoubled, declearer, tricks, lead_level, lead_suit, score, egge_enum, pair_score_id) "
        "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (board.board_number, board.opponents[0], board.opponents[1], board.contract.contract_level,
         board.contract.suit.name, int(board.contract.doubled), int(board.contract.redoubled), board.declearer,
         board.tricks, board.lead_level, board.lead_suit.name, board.score, board.egge_enum.name, pair_stat_id))


def get_all_pair_boards(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM pair_board")
    return c.fetchall()


def get_all_tournaments(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM tournament")
    return c.fetchall()


def get_all_clubs(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM club")
    return c.fetchall()


def get_all_pair_boards_for_pairs(database, players):
    conn = create_connection(database)
    c = conn.cursor()
    c.execute("SELECT * FROM pair_board pb "
              "JOIN pair_score ps "
              "ON pb.pair_score_id = ps.id "
              "WHERE ps.player_name1 IN (?, ?) "
              "AND ps.player_name2 IN (?, ?);", (players[0], players[1], players[0], players[1]))
    return c.fetchall()


def main():
    database = "C:\\Users\Joppe\PycharmProjects\Eggeliste\src\db\db.db"
    sql_create_club = "CREATE TABLE IF NOT EXISTS club (id INTEGER PRIMARY KEY,name TEXT NOT NULL,url TEXT NOT NULL)"
    sql_create_tournament = "CREATE TABLE IF NOT EXISTS tournament (id INTEGER PRIMARY KEY,title TEXT,club_id INTEGER,url TEXT NOT NULL,date TEXT,rounds INTEGER, boards INTEGER,pairs INTEGER, tournament_type TEXT, FOREIGN KEY(club_id) REFERENCES club(id))"
    sql_create_pair_score = "CREATE TABLE IF NOT EXISTS pair_score (id INTEGER PRIMARY KEY,player_name1 TEXT,player_name2 TEXT,club_name1 TEXT,club_name2 TEXT,points REAL,score REAL,tournament_id INTEGER NOT NULL,FOREIGN KEY(tournament_id) REFERENCES tournament(id))"
    sql_create_pair_board = "CREATE TABLE IF NOT EXISTS pair_board (id INTEGER PRIMARY KEY,board_number INTEGER,opponent_name1 TEXT,opponent_name2 TEXT,contract_level INTEGER,contract_suit TEXT,doubled INTEGER,redoubled INTEGER,declearer TEXT,tricks INTEGER,lead_level INTEGER,lead_suit TEXT,score REAL,egge_enum TEXT,pair_score_id INTEGER,FOREIGN KEY(pair_score_id) REFERENCES pair_score(id))"

    conn = create_connection(database)

    create_table(conn, sql_create_club)
    create_table(conn, sql_create_tournament)
    create_table(conn, sql_create_pair_score)
    create_table(conn, sql_create_pair_board)


if __name__ == '__main__':
    main()
