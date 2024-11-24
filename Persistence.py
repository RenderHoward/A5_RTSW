import sqlite3

class Store:
    def __init__(self, db, tbl):
        self.database = db
        self.table = tbl
        self.con = sqlite3.connect(self.database)
        self.insrtstr = "INSERT INTO " + self.table + " (time_tag, speed, density, temperature, bx, by, bz, bt, vx, vy, vz, propagated_time_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"

    def begintrans(self):
        self.cursor = self.con.cursor()

    def addrecord(self, rec):
        self.cursor.execute(self.insrtstr, rec)

    def endtrans(self):
        self.con.commit()

