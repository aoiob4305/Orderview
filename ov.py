#-*- coding: utf-8 -*-

from flask import Flask, render_template
from datetime import datetime
import ovsql

app = Flask(__name__)

@app.route("/")
@app.route("/<plant>")
def main(plant=None):
    today = datetime.now().strftime("%Y%m%d")
    status, results = ovsql.getOrderDataTargetDate(today)
    if not (status is False):
        results = ovsql.convEncoding(results, 'ISO-8859-1', 'euc-kr')
    
    # 플랜트 데이터 추가
    for result in results:
        result['plant'] = ovsql.getWhichPlant(result['equiCode'])

    return render_template("main.html", results=results, plant=plant)

if __name__ == '__main__':
    app.run(port=8888, debug=True)