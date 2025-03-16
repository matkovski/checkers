import sqlite3

class DbService:
    def __init__(self):
        self.con = sqlite3.connect("data/games.db")
        self.cursor = self.con.cursor()

        self.initialise()
    
    def initialise(self):
        try:
            self.cursor.execute('select count(*) from games')
        except:
            self.cursor.execute('create table games (id, white, black, end, moves)')
            self.cursor.execute('create table users (id, login, pwd, code)')

    def query(self, sql, params = None):
        res = self.cursor.execute(sql, params)
        return res.fetchall()

    def row(self, sql, params = None):
        res = self.cursor.execute(sql, params)
        return res.fetchone()
    
    def run(self, sql, params = None):
        self.cursor.execute(sql, params)
        self.con.commit()

db = DbService()
