#-*- coding: utf-8 -*-

from flask import Flask, render_template
import ovsql

app = Flask(__name__)

@app.route("/")
def main():
    results = ovsql.convEncoding(ovsql.getData("20180515"),'ISO-8859-1','euc-kr')
    return render_template("main.html", results=results)

if __name__ == '__main__':
    app.run(port=8888, debug=True)
