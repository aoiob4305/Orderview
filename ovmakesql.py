#-*- coding:utf-8 -*-

import sqlite3
from ovsql import getMcData, convEncoding

database = "test.db"

connection = sqlite3.connect(database)
cursor = connection.executescript('''
    create table if not exists mcList (
        mc_id integer primary key autoincrement,
        McCode,
        Mc_Name,
        MaintPart
    );
    ''')

connection.commit()

results = convEncoding(getMcData()[1],'ISO-8859-1','euc-kr')

sql = '''INSERT INTO mcList(McCode,Mc_Name,MaintPart) values (?,?,?)'''
for result in results:
    r = cursor.execute(sql, (result[0], result[1], result[2]))

connection.commit()
connection.close()

print('adding %d items.' % len(results))

class mcListDB:
    def __init__(self,db):
        self.data = threading.local()
        self.db = db
        self._initdb()

    def connect(self):
        self.data.conn = sqlite3.connect(self.db)
        self.data.conn.row_factory = sqlite3.Row

    def _initdb(self):
        conn = sqlite3.connect(self.db)
        conn.cursor().executescript('''
            create table if not exists mcList (
                mc_id integer primary key autoincrement,
                McCode,
                Mc_Name,
                MaintPart
            );
        ''')
        conn.commit()
        conn.close()