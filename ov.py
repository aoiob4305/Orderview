#-*- coding: utf-8 -*-

from flask import Flask, render_template
from datetime import datetime
import ovsql

app = Flask(__name__)

@app.route("/")
def main():
#    results = ovsql.convEncoding(ovsql.getOrderDataTargetDate("20180515"),'ISO-8859-1','euc-kr')
    today = datetime.now().strftime("%Y%m%d")
    status, results = ovsql.getOrderDataTargetDate(today)
    if not (status is False):
        results = ovsql.convEncoding(results, 'ISO-8859-1', 'euc-kr')
    return render_template("main.html", results=results)

if __name__ == '__main__':
    app.run(port=8888, debug=True)
