#-*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
    return "hello"

if __name__ == '__main__':
    app.run(port=8888, debug=True)