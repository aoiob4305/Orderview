#-*- coding: utf-8 -*-

import pymssql
import sqlite3

#서버 주소 및 정보 
SERVER="10.214.100.73" 
USER="PM_EQ" 
PASSWORD="pm_Eq1@" 
MSSQLDB="PM_EUQI_NOTI" 

def sendQueryToServer(server, user, password, database, sqlquery):
    try:
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
        cursor = conn.cursor()
        cursor.execute(sqlquery)
        fetchResult = cursor.fetchall()
        conn.close()

    except pymssql.Error as e:
       print("SQL Error: "+str(e))
       fetchResult = [False, 'Error']

    return [True, fetchResult]

# 특정일 고장 데이터 뽑기
def getOrderDataTargetDate(targetDate):
    SQLQUERY = "SELECT equiName,notiContent,notiDate,notiTime,equiCode,order_con FROM PM01_EuqiNotify WHERE notiDate='"+targetDate+"' ORDER BY notiTime DESC"
    
    results = sendQueryToServer(SERVER, USER, PASSWORD, MSSQLDB, SQLQUERY)
    return results

def getMcData():
    SQLQUERY = "SELECT McCode, Mc_Name, MaintPart FROM PM01_McMaster ORDER BY McCode ASC"

    results = sendQueryToServer(SERVER, USER, PASSWORD, MSSQLDB, SQLQUERY)
    return results

# 인코딩이 문제라 변환해준다.
# item은 쿼리 출력값
def convEncoding(items, code1, code2):
    results = []
    for item in items:
        result = ()
        for t in item:
            try:
                result = result + (t.encode(code1).decode(code2),)
            except:
                result = result + ('',)
        results.append(result)

    return results

mcDB = "test.db"
#local mcdata check
def getWhichPlant(mcCode):
    conn = sqlite3.connect(mcDB)
    cur = conn.cursor()
    sql = '''SELECT * FROM mcList WHERE McCode = ?'''

    cur.execute(sql, (mcCode,))
    result = cur.fetchall()[0][3]
    
    if result is None:
        result = "N/A"

    return result