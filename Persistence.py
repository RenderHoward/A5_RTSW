import sqlite3
from pathlib import Path


class Store:
    def __init__(self, db, url):
        self.database = db
        self.table = self.__URL2TblName(url)
        self.con = sqlite3.connect(self.database)
        self.insrtstr = "INSERT INTO " + self.table + " (time_tag, speed, density, temperature, bx, by, bz, bt, vx, vy, vz, propagated_time_tag) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)"

        if self.tableexists():
            self.__init_strs()

    def begintrans(self):
        self.cursor = self.con.cursor()

    def addrecord(self, rec):
        self.cursor.execute(self.insrtstr, rec)

    def endtrans(self):
        self.con.commit()

    def tableexists(self) -> bool:
        cur = self.con.cursor()
        count = cur.execute("select count(*) from URL2TBL where TBLName = ? COLLATE NOCASE", [self.table] ).fetchone()[0]
        cur.close()
        return count == 1

    def __URL2TblName( self, url ) -> str:
        return Path(url).stem.replace('-', '_')
    def addtable(self, urlstr, data):
        if self.tableexists():
            return

        tblname = self.__URL2TblName(urlstr)

        query = "create table " + self.table + " ( "

        names = data[0]

        for field in names:
            query += field
            if "time" in field :
                query += " TEXT, "
            else:
                query += " REAL, "

        query = query.rstrip(", ")

        query += " )"

        cur = self.con.cursor()

        cur.execute(query)

        query = "INSERT INTO URL2TBL (TblName, URL, InsertStr) values (?, ?, ?)"

        insertstr = "(" + ", ".join(names) + ") values (" + ", ".join(['?'] * len(names)) + ")"

        cur.execute(query, [tblname, urlstr, insertstr])

        cur.close()

        self.con.commit()

        self.insrtstr = "INSERT INTO " + self.table + " " + insertstr

        self.begintrans()

        for rec in data[1:]:
            self.addrecord(rec)

        self.endtrans()

        self.endtrans()

