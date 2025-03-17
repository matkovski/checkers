import sqlite3

class DbService:
    def __init__(self):
        self.con = sqlite3.connect("data/checkers.db")

        self.initialise()
    
    def initialise(self):
        cursor = self.con.cursor()

        try:
            cursor.execute('select count(*) from games')
        except:
            cursor.execute('create table games (id, white, black, end, moves)')
            cursor.execute('create table users (id, login, pwd, code)')
        
        cursor.close()

    def query(self, sql, params = None):
        cursor = self.con.cursor()
        res = cursor.execute(sql, params)
        data = res.fetchall()
        cursor.close()
        return data

    def row(self, sql, params = None):
        cursor = self.con.cursor()
        res = cursor.execute(sql, params)
        data = res.fetchone()
        cursor.close()
        return data
    
    def run(self, sql, params = None):
        cursor = self.con.cursor()
        cursor.execute(sql, params)
        self.con.commit()
        cursor.close()

db = DbService()
