import sqlite3
from http.cookiejar import UTC_ZONES
from pathlib import Path

from future.backports.datetime import datetime


class Store:
    def __init__(self, db, url):
        self.database = db
        self.table = self.__URL2TblName(url)
        self.con = sqlite3.connect(self.database)
        self.con.row_factory = sqlite3.Row

        self.earliest = self.latest = self.insrtstr = self.URL = ""

        if self.tableexists():
            self.__init_strs()

    def begintrans(self):
        self.cursor = self.con.cursor()

    def addrecord(self, rec):
        self.cursor.execute(self.insrtstr, rec)

    def endtrans(self):
        self.con.commit()
        self.refreshtimebracket()

    def __init_strs(self) :
        cur = self.con.cursor()
        result = cur.execute( "select * from URL2TBL where TblName = ?", [self.table]).fetchone()
        cur.close()
        self.insrtstr = "INSERT INTO " + self.table + " " + result["InsertStr"]
        self.URL = result["URL"]
        self.refreshtimebracket()

    def tableexists(self) -> bool:
        cur = self.con.cursor()
        count = cur.execute("select count(*) from URL2TBL where TBLName = ? COLLATE NOCASE", [self.table] ).fetchone()[0]
        cur.close()
        return count == 1

    def __URL2TblName( self, url ) -> str:
        return Path(url).stem.replace('-', '_')

    def refreshtimebracket(self):
        cur = self.con.cursor()
        bounds = cur.execute("select max(time_tag) as end, min(time_tag) as begin from " + self.table).fetchone()
        self.earliest = bounds["begin"]
        self.latest   = bounds["end"]
        cur.close()

    def bracket(self, timestamp)-> []:
        self.refreshtimebracket()

        if timestamp > self.latest :
            return [{ "error" : "no data yet" }]

        if timestamp < self.earliest :
            return [{ "error" : "data not recorded that early" }]

        cur = self.con.cursor()

        compound_query = "select * from " + self.table + \
                    " where time_tag between " +\
                    "(" +\
                    "	select max(time_tag) from " + self.table +\
                    "	where time_tag < ?  " +\
                    ")" +\
                    "and" +\
                    "(" +\
                    "	select min(time_tag) from " + self.table +\
                    "	where time_tag >= ? " +\
                    ")"

        bounds = cur.execute( compound_query , [timestamp, timestamp]  ).fetchall()
        cur.close()

        return [ {k: row[k] for k in row.keys()} for row in bounds ]

    def recordsbetween(self, starttime, endtime):
        self.refreshtimebracket()

        endtime = min(endtime, self.latest)

        starttime = max(starttime, self.earliest)

        cur = self.con.cursor()

        results = cur.execute("select * from " + self.table + " where time_tag between ? and ? ", [starttime, endtime])

        rows = results.fetchall()

        return [rows[0].keys()] + [[row[k] for k in row.keys()] for row in rows]

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

