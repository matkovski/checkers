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
            cursor.execute('create table sessions (id str primary key, userid integer, expires float)')
            cursor.execute('create table users (id integer primary key, login varchar(100), pwd varchar(100), code varchar(100))')
            cursor.execute('create table games (id integer primary key, white integer, black integer, end char(1), moves text)')
        
        cursor.close()

    def query(self, sql, params = None):
        cursor = self.con.cursor()
        res = cursor.execute(sql, params)
        data = res.fetchall()
        cursor.close()
        return data

    def row(self, sql, params = None):
        cursor = self.con.cursor()
        res = cursor.execute(sql, params or {})
        data = res.fetchone()
        cursor.close()
        return data
    
    def run(self, sql, params = None):
        cursor = self.con.cursor()
        cursor.execute(sql, params)
        self.con.commit()
        cursor.close()

db = DbService()
