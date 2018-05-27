from flask import Flask
from flask import jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
from mysql.connector import connection
from database import *
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/se2018/CS304-A-web-platform-for-data-labelling/upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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
    password = c.get_user_passwd(user_email=user_email)
    if password is not None:
        if password == pass_word:
            result = {'code': 0}
        elif password != pass_word:
            result = {'code': 1, 'message': 'Wrong password!'}
    else:
        result = {'code': 1, 'message': 'User doesn\'t exist!'}
    return jsonify(result)


@app.route('/register/email/<user_email>/username/<user_name>/password/<pass_word>')
@cross_origin()
def email_register(user_name, user_email, pass_word):
    result = c.insert_user(username=user_name, user_email=user_email, passwd=pass_word, signin_time=get_timestamp(), credits=0)
    if result == 1:
        return jsonify({'code': 0})
    elif result == 0:
        result = {'code': 1, 'message': 'User already exists!'}
    else:
        result = {'code': 1, 'message': 'Register failed! Please try later!'}
    return jsonify(result)


@app.route('/forget/email/<user_email>')
@cross_origin()
def email_forget(user_email):
    result = c.user_exist(user_email=user_email)
    if result:
        return jsonify({'code': 0})
    else:
        return jsonify({'code': 1, 'message': 'User doesn\'t exist!'})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('no filename')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port="5000", debug=True)
