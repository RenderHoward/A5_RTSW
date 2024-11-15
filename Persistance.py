import sqlite3

class Store:

    def __init__(self, db, tbl):
        self.database = db
        self.table = tbl
        self.con = sqlite3.connect(self.database)

    def addrecord(self, rec):
        print(rec)
        # cursor = con.cursor()



