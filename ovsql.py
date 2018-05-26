#-*- coding: utf-8 -*-

import pymssql
import sqlite3
from configparser import ConfigParser

config = ConfigParser()
config.read("config.ini")

SERVER=config['SERVER']['SERVER']
USER=config['SERVER']['USER']
PASSWORD=config['SERVER']['PASSWORD']
MSSQLDB=config['SERVER']['MSSQLDB']

def sendQueryToServer(sqlquery):
    print (SERVER, USER, PASSWORD, MSSQLDB)
    with pymssql.connect(server=SERVER, user=USER, password=PASSWORD, database=MSSQLDB) as conn:
        with conn.cursor(as_dict=True) as cursor:
            try:
                cursor.execute(sqlquery)
                fetchResult = [True, cursor.fetchall()]
            except pymssql.Error as e:
                print("SQL Error: "+str(e))
                fetchResult = [False, 'Error']

    return fetchResult

# 특정일 고장 데이터 뽑기
def getOrderDataTargetDate(targetDate):
    SQLQUERY = "SELECT equiName,notiContent,notiDate,notiTime,equiCode,order_con FROM PM01_EuqiNotify WHERE notiDate='"+targetDate+"' ORDER BY notiTime DESC"
    
    results = sendQueryToServer(SQLQUERY)
    return results

def getMcData():
    SQLQUERY = "SELECT McCode, Mc_Name, MaintPart FROM PM01_McMaster ORDER BY McCode ASC"

    results = sendQueryToServer(SQLQUERY)
    return results

# 인코딩이 문제라 변환해준다.
# item은 쿼리 출력값
def convEncoding(items, code1, code2):
    results = []
    for item in items:
        result = {}
        for key in item.keys():
            try:
                result[key] = item[key].encode(code1).decode(code2)
            except:
                result[key] = ''
        results.append(result)

    return results

#local mcdata check
mcDB = "test.db"
def getWhichPlant(mcCode):
    conn = sqlite3.connect(mcDB)
    cur = conn.cursor()
    sql = '''SELECT * FROM mcList WHERE McCode = ?'''

    cur.execute(sql, (mcCode,))
    result = cur.fetchall()[0][3]
    
    if result is None:
        result = "N/A"

    return result