from flask import Flask
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
from mysql.connector import connection
from database import *



app = Flask(__name__)
CORS(app)
cnx = connection.MySQLConnection(user='root',
                                 password='se2018',
                                 host='127.0.0.1',
                                 database='se_proj')
c = sql_conn(cnx)


@app.route("/")
@cross_origin()
def index_void():
    return render_template('index.html')


@app.route("/index.html")
@cross_origin()
def index():
    return render_template('index.html')


@app.route("/login.html")
@cross_origin()
def login():
    return render_template('login.html')


@app.route("/mainpage.html")
@cross_origin()
def mainpage():
    return render_template('mainpage.html')


@app.route("/imagelabel.html")
@cross_origin()
def imagelabel():
    return render_template('imagelabel.html')


@app.route("/publish.html")
@cross_origin()
def publish():
    return render_template('publish.html')


@app.route("/textlabel.html")
@cross_origin()
def textlabel():
    return render_template('textlabel.html')


@app.route("/textlabel2.html")
@cross_origin()
def textlabel2():
    return render_template('textlabel2.html')


@app.route('/login/username/<user_name>/password/<pass_word>')
@cross_origin()
def username_login(user_name, pass_word):
    password = c.get_user_passwd(username=user_name)
    if password is not None:
        if password == pass_word:
            result = {'code': 0}
        elif password != pass_word:
            result = {'code': 1, 'message': 'Wrong password!'}
    else:
        result = {'code': 1, 'message': 'User doesn\'t exist!'}
    return jsonify(result)

@app.route('/login/email/<user_email>/password/<pass_word>')
@cross_origin()
def email_login(user_email, pass_word):
    password = c.get_user_passwd(useremail=user_email)
    if password is not None:
        if password == pass_word:
            result = {'code': 0}
        elif password != pass_word:
            result = {'code': 1, 'message': 'Wrong password!'}
    else:
        result = {'code': 1, 'message': 'User doesn\'t exist!'}
    return jsonify(result)

if __name__ == '__main__':
   app.run(host="0.0.0.0", port="5000", debug=True)
