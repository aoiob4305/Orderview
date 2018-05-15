#-*- coding: utf-8 -*-

import pymssql

#서버 주소 및 정보
SERVER="10.214.100.73"
USER="PM_EQ"
PASSWORD="pm_Eq1@"
DATABASE="PM_EUQI_NOTI"

def sendQueryToServer(server, user, password, database, sqlquery):
    try:
        conn = pymssql.connect(server=server, user=user, password=password, database=database)
    except pymssql.Error as e:
       print("SQL Error: "+str(e))
       fetchResult = [False, 'Connection Error']

    cursor = conn.cursor()

    try:
        cursor.execute(sqlquery)
        fetchResult = cursor.fetchall()
    except pymssql.Error as e:
        print("SQL Error: "+str(e))
        conn.close()
        fetchResult = [False, 'Query Error']

    conn.close()

    return [True, fetchResult]

# 특정일 고장 데이터 뽑기
def getOrderDataTargetDate(targetDate):
    SQLQUERY = "SELECT equiName,notiContent,notiDate,notiTime,equiCode,order_con FROM PM01_EuqiNotify WHERE notiDate='"+targetDate+"' ORDER BY notiTime ASC"
    
    results = sendQueryToServer(SERVER, USER, PASSWORD, DATABASE, SQLQUERY)
    return results

def getMcData():
    SQLQUERY = "SELECT McCode, Mc_Name, MaintPart FROM PM01_McMaster ORDER BY McCode ASC"

    results = sendQueryToServer(SERVER, USER, PASSWORD, DATABASE, SQLQUERY)
    return results

# 인코딩이 문제라 변환해준다.
# item은 쿼리 출력값
def convEncoding(items, code1, code2):
    results = []
    for item in items:
        result = {'equiName': item[0].encode(code1).decode(code2),
                'notiContent': item[1].encode(code1).decode(code2),
                'notiDate': item[2].encode(code1).decode(code2),
                'notiTime': item[3].encode(code1).decode(code2),
                'equiCode': item[4].encode(code1).decode(code2),
                'order_con': item[5].encode(code1).decode(code2)}
        results.append(result)

    return results
