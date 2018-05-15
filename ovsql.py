#-*- coding: utf-8 -*-

import pymssql

SERVER="10.214.100.73"
USER="PM_EQ"
PASSWORD="pm_Eq1@"
DATABASE="PM_EUQI_NOTI"

def getData(targetDate):
    SQLCOMMAND="SELECT equiName,notiContent,notiDate,notiTime FROM PM01_EuqiNotify WHERE notiDate='"+targetDate+"' ORDER BY notiTime DESC"
    try:
        conn = pymssql.connect(server=SERVER, user=USER, password=PASSWORD, database=DATABASE)
    except pymssql.Error as e:
       print("SQL Error: "+str(e))

    cursor = conn.cursor()

    try:
        cursor.execute(SQLCOMMAND)
    except pymssql.Error as e:
        print("SQL Error: "+str(e))
        conn.close()
        exit()

    fetchResult = cursor.fetchall()
    conn.close()

    return fetchResult

def convEncoding(items, code1, code2):
    results = []
    for item in items:
        result = {'equiName': item[0].encode(code1).decode(code2),
                'notiContent': item[1].encode(code1).decode(code2),
                'notiDate': item[2].encode(code1).decode(code2),
                'notiTime': item[3].encode(code1).decode(code2)}
        results.append(result)

    return results
