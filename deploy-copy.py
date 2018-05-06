from flask import Flask
from flask import jsonify
from flask import render_template
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from time import gmtime, strftime
from sql_query import *


server =  SSHTunnelForwarder(
     ('47.106.34.103', 22),
     ssh_password="se2018",
     ssh_username="se2018",
     remote_bind_address=('127.0.0.1', 3306))
server.start()
engine = create_engine('mysql+mysqldb://root:se2018@127.0.0.1:%s/se_proj' % server.local_bind_port)
connection = engine.connect()

c = sql_conn(connection)

app = Flask(__name__)


@app.route("/")
def index_void():
    return render_template('index.html')

@app.route("/index.html")
def index():
    return render_template('index.html')

@app.route("/login.html")
def login():
    return render_template('login.html')

@app.route("/mainpage.html")
def mainpage():
    return render_template('mainpage.html')

@app.route("/imagelabel.html")
def imagelabel():
    return render_template('imagelabel.html')

@app.route("/publish.html")
def publish():
    return render_template('publish.html')

@app.route("/textlabel.html")
def textlabel():
    return render_template('textlabel.html')

@app.route("/textlabel2.html")
def textlabel2():
    return render_template('textlabel2.html')

@app.route('/login/username/<user_name>/password/<pass_word>')
def verification(user_name, pass_word):
    if str(c.get_user_passwd(user_name)) == pass_word:
        verification = {'code': 0}
    elif str(c.get_user_passwd(user_name)) != pass_word:
        verification = {'code': 1}
    return jsonify(verification)