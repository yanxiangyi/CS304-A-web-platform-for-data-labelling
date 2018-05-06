from flask import Flask
from flask import jsonify
from flask import render_template
import MySQLdb

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/mainpage")
def mainpage():
    return render_template('mainpage.html')

@app.route('/test1')
def summary():
    return jsonify("a")

@app.route('/login/username/<user_name>/password/<pass_word>')
def verification(user_name, pass_word):
    conn = MySQLdb.connect(host='127.0.0.1',user="root",passwd="se2018",db="se_proj")
    cur = conn.cursor()
    cur.execute('select * from users;')
    print("aaa")
    for row in cur:
        if row[1] == user_name:
            if row[2] == pass_word:
                verification = {'code':0}
            elif row[2] != pass_word:
                verification = {'code':1}
    return jsonify(verification)