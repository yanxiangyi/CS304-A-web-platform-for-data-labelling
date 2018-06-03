from flask import Flask, jsonify, render_template, session, redirect, url_for, escape, request, send_from_directory
from flask_cors import CORS, cross_origin
from mysql.connector import connection
from database import *
import os
import zipfile
import datetime
import shutil
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = '/home/se2018/CS304-A-web-platform-for-data-labelling/upload'
EXTRACT_FOLDER = '/home/se2018/data'
ALLOWED_EXTENSIONS = set(['zip'])

app = Flask(__name__)
app.secret_key = 'any random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'any random string'
CORS(app)
# cnx = connection.MySQLConnection(user='root',
#                                  password='se2018',
#                                  host='127.0.0.1',
#                                  database='se_proj')
# c = sql_conn(cnx)


def init_cnx():
    cnx = connection.MySQLConnection(user='root',
                                     password='se2018',
                                     host='127.0.0.1',
                                     database='se_proj')
    c = sql_conn(cnx)
    return c


@app.route("/index.html")
@cross_origin()
def index():
    return redirect(url_for('index_void'))


@app.route("/")
@cross_origin()
def index_void():
    if 'email' in session:
        if session['level'] == 0:
            return render_template('index.html')
        elif session['level'] == 1:
            return render_template('indexA1.html')
        else:
            return render_template('indexAX.html')
    return redirect(url_for('mainpage'))


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('email', None)
    return redirect(url_for('logout_page'))


@app.route("/logout.html")
@cross_origin()
def logout_page():
    return render_template("logout.html")


@app.route("/login.html", methods=['GET', 'POST'])
@cross_origin()
def login():
    return render_template('login.html')


@app.route("/register.html")
@cross_origin()
def register():
    return render_template('register.html')


@app.route("/mainpage.html")
@cross_origin()
def mainpage():
    return render_template('mainpage.html')


@app.route("/choose.html")
@cross_origin()
def choose():
    if "email" not in session:
        result = {"code": 1, "message": "Please login first!"}
        return jsonify(result)
    else:
        if session['level'] != 0:
            result = {"code": 1, "message": "Please login as users!"}
            return jsonify(result)
        else:
            return render_template('choose.html')


@app.route("/imagelabel.html")
@cross_origin()
def imagelabel():
    return render_template('imagelabel.html')


@app.route("/textlabel.html")
@cross_origin()
def textlabel():
    return render_template('textlabel.html')


@app.route('/login_admin/email/<admin_email>/password/<pass_word>')
@cross_origin()
def email_login_admin(admin_email, pass_word):
    c = init_cnx()
    password = c.get_admin_passwd(admin_email=admin_email)
    c.close()
    if password is not None:
        if password == pass_word:
            result = {'code': 0}
            session['email'] = admin_email
            c = init_cnx()
            level = c.get_admin_access_level(admin_email=admin_email)
            c.close()
            if level == 1:
                session['level'] = 1
            else:
                session['level'] = 2
        elif password != pass_word:
            result = {'code': 1, 'message': 'Wrong password!'}
    else:
        result = {'code': 1, 'message': 'Admin doesn\'t exist!'}
    return jsonify(result)


@app.route('/login/email/<user_email>/password/<pass_word>')
@cross_origin()
def email_login(user_email, pass_word):
    c = init_cnx()
    password = c.get_user_passwd(user_email=user_email)
    c.close()
    if password is not None:
        if password == pass_word:
            result = {'code': 0}
            session['level'] = 0
            session['email'] = user_email
        elif password != pass_word:
            result = {'code': 1, 'message': 'Wrong password!'}
    else:
        result = {'code': 1, 'message': 'User doesn\'t exist!'}
    return jsonify(result)


@app.route('/register/email/<user_email>/username/<user_name>/password/<pass_word>')
@cross_origin()
def email_register(user_name, user_email, pass_word):
    c = init_cnx()
    result = c.insert_user(username=user_name, user_email=user_email, passwd=pass_word, signin_time=get_timestamp(), credits=0)
    c.close()
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
    c = init_cnx()
    result = c.user_exist(user_email=user_email)
    c.close()
    if result:
        return jsonify({'code': 0})
    else:
        return jsonify({'code': 1, 'message': 'User doesn\'t exist!'})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/publish.html', methods=['GET', 'POST'])
@cross_origin()
def upload_file():
    if 'email' not in session:
        result = {"code": 1, "message": "Please login first!"}
        return jsonify(result)
    else:
        if session['level'] == 0:
            result = {"code": 1, "message": "Users can't publish tasks!"}
            return jsonify(result)
        else:
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
                    # Save file
                    filename = secure_filename(file.filename)
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(save_path)
                    # Unzip file to the 'EXTRACT_FOLDER/projectName_timeStamp'
                    zip_ref = zipfile.ZipFile(save_path, 'r')
                    final_path = os.path.join(EXTRACT_FOLDER, filename.split(".zip")[0] + "_" + datetime.datetime.today().strftime('%Y-%m-%d'))
                    if not os.path.exists(final_path):
                        os.makedirs(final_path)
                    zip_ref.extractall(final_path)
                    zip_ref.close()
                    # Only keep Json files
                    for filename in os.listdir(final_path):
                        if not os.path.join(final_path, filename).endswith(".json"):
                            if os.path.isdir(os.path.join(final_path, filename)):
                                shutil.rmtree(os.path.join(final_path, filename))
                            else:
                                os.remove(os.path.join(final_path, filename))
                        elif filename == "meta.json":
                            with open(os.path.join(final_path, filename)) as f:
                                meta = json.load(f)
                                sourcename = meta['projectName']
                                description = meta['description']
                            f.close()
                            os.remove(os.path.join(final_path, filename))
                    # root_path = os.path.join(EXTRACT_FOLDER,
                    # sourcename + "_" + datetime.datetime.today().strftime('%Y-%m-%d'))
                    # os.renames(final_path, root_path)
                    root_path = final_path
                    admin_email = session['email']
                    c = init_cnx()
                    admin_id = c.get_admin_id(admin_email=admin_email)
                    c.close()
                    result = {"code": 0}
                    c = init_cnx()
                    insert = c.insert_source(sourcename=sourcename, finished=0, publisher=admin_id, description=description, publish_time=get_timestamp(), priority=1)
                    c.close()
                    if insert == -1:
                        result = {"code": 1, "message": "Task insertion failed!"}
                    else:
                        c = init_cnx()
                        load = c.load_data(root_path=root_path, sourcename=sourcename)
                        c.close()
                        if load == 0:
                            result = {"code": 1, "message": "Data insertion failed!"}
                    return jsonify(result)
    return render_template('publish.html')


@app.route('/profile')
@cross_origin()
def profile():
    if 'email' in session:
        email = session['email']
        if session['email'] != email:
            result = {"code": 1, "message": "Please login first!"}
            return jsonify(result)
        if session['level'] == 0:
            c = init_cnx()
            if c.user_exist(user_email=email):
                [user_id, user_email, user_name, password, signup_time, user_credit, num_answer, num_acc, num_val, num_val_tp] = c.get_user(user_email=email)
                user_num = c.get_user_number()
                source_involved = len(c.get_user_source(user_email=email))
                rank = c.get_user_credit_rank(user_email=email)
                source_number = c.get_source_number()
                result = {"user_id": user_id, "user_email": user_email,
                          "user_name": user_name, "user_credit": user_credit,
                          "num_acc": num_acc, "num_answer": num_answer,
                          "signup_time": signup_time, "num_val": num_val,
                          "num_val_tp": num_val_tp, "rank": 1-(float(rank-1)/float(user_num)),
                          "percentage_involved": float(source_involved)/float(source_number)}
                result = {"code": 0, "message": result}
            else:
                result = {"code": 1, "message": "User doesn\'t exist!"}
            c.close()
        else:
            c = init_cnx()
            [admin_id, admin_email, admin_name, password, level] = c.get_admin(admin_email=email)
            c.close()
            result = {
                "user_id": admin_id, "user_email": admin_email,
                "user_name": admin_name, "user_level": level
            }
            result = {"code": 0, "message": result}
    else:
        result = {"code": 1, "message": "Please login first!"}
    return jsonify(result)


@app.route('/recent_task')
@cross_origin()
def recent_task():
    # if "email" in session:
    c = init_cnx()
    source_number = c.get_source_number()
    all_source = c.get_recent_source(limit=5)
    c.close()
    tasks = []
    for source in all_source:
        [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
        date = datetime.datetime.fromtimestamp(publish_date)
        task = {"publisher": publisher,
                "publish_date": str(date.month) + "." + str(date.day),
                "source_name": source_name,
                "num_finished": finished,
                "source_id": source_id,
                "description": description,
                "priority": priority,
                "number": num_json
        }
        tasks.append(task)
    result = {"code": 0,
              "message": {
                  "task_num": source_number,
                  "tasks": tasks
              }
              }
    # else:
    #     result = {"code": 1,
    #               "message": "Please login first!"
    #               }

    return jsonify(result)


@app.route('/task')
@cross_origin()
def task():
    if "email" in session:
        if session['level'] == 2:
            c = init_cnx()
            source_number = c.get_source_number()
            c.close()
            c = init_cnx()
            all_source = c.get_all_source()
            c.close()
            tasks = []
            for source in all_source:
                [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
                task = {"publisher": publisher,
                        "publish_date": publish_date,
                        "source_name": source_name,
                        "num_finished": finished,
                        "source_id": source_id,
                        "description": description,
                        "priority": priority,
                        "number": num_json
                }
                tasks.append(task)
            result = {"code": 0,
                      "message": {
                          "task_num": source_number,
                          "tasks": tasks
                      }
                      }

        elif session['level'] == 1:
            c = init_cnx()
            all_source = c.get_all_source()
            c.close()
            tasks = []
            admin_email = session['email']
            for source in all_source:
                [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
                c = init_cnx()
                if publisher == c.get_admin_id(admin_email=admin_email):
                    c.close()
                    task = {"publisher": publisher,
                            "publish_date": publish_date,
                            "source_name": source_name,
                            "num_finished": finished,
                            "source_id": source_id,
                            "description": description,
                            "priority": priority,
                            "number": num_json
                            }
                    tasks.append(task)
            source_number = len(tasks)
            result = {"code": 0,
                      "message": {
                          "task_num": source_number,
                          "tasks": tasks
                      }
                      }

        else:
            c = init_cnx()
            source_number = c.get_source_number()
            all_source = c.get_all_source()
            c.close()
            tasks = []
            for source in all_source:
                [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
                task = {"publisher": publisher,
                        "publish_date": publish_date,
                        "source_name": source_name,
                        "num_finished": finished,
                        "source_id": source_id,
                        "description": description,
                        "priority": priority,
                        "number": num_json
                }
                tasks.append(task)
            result = {"code": 0,
                      "message": {
                          "task_num": source_number,
                          "tasks": tasks
                      }
                      }
    else:
        result = {"code": 1,
                  "message": "Please login first!"
                  }

    #     [user_id, user_email, user_name, password, signup_time, user_credit, num_total, num_acc, num_examined] = c.get_source_number()
    #     result = {"user_id": user_id, "user_email": user_email,
    #               "user_name": user_name, "user_credit": user_credit,
    #               "num_acc": num_acc, "num_total": num_total,
    #               "signup_time": signup_time, "num_examined": num_examined}
    #     result = {"code": 0, "message": result}
    # else:
    #     result = {"code": 1, "message": "User doesn\'t exist!"}
    return jsonify(result)

#
# @app.route('/task1')
# @cross_origin()
# def task1():
#     c = init_cnx()
#     source_number = c.get_source_number()
#     all_source = c.get_all_source()
#     c.close()
#     tasks = []
#     for source in all_source:
#         [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
#         task = {"publisher": publisher,
#                 "publish_date": publish_date,
#                 "source_name": source_name,
#                 "num_finished": finished,
#                 "source_id": source_id,
#                 "description": description,
#                 "priority": priority,
#                 "number": num_json
#                 }
#         tasks.append(task)
#     result = {"code": 0,
#               "message": {
#                   "task_num": source_number,
#                   "tasks": tasks
#               }
#               }
#     return jsonify(result)


@app.route('/data/<sourcename>')
@cross_origin()
def send_data(sourcename):
    if "email" in session:
        if session['level'] == 0:
            if 'jsons' not in session:
                email = session['email']
                c = init_cnx()
                jsons = c.fetch_data(sourcename=sourcename, user_email=email, nb=5)
                c.close()
                session['jsons'] = jsons
            else:
                jsons = session['jsons']
            result = {"code": 0, "message": jsons}
        else:
            result = {"code": 1, "message": "Please login as users!"}
    else:
        result = {"code": 1, "message": "Please login first!"}
    return jsonify(result)


@app.route('/retrieve', methods=['GET', 'POST'])
@cross_origin()
def retrieve_label():
    if "email" in session:
        if session['level'] == 0:
            if 'jsons' in session:
                content = request.get_json(silent=True)
                content = {
  "code": 0,
  "message": [
    {
      "data": "\u8c22\u4e39\u5b81\u771f\u6f02\u4eae",
      "dataid": 34,
      "index": 1,
      "projectName": "xiedn_proj",
      "task": [
        {
          "aim": "",
          "choices": [
            "Positive",
            "Neutral",
            "Negative"
          ],
          "front": "option",
          "label": "",
          "mode": "single"
        }
      ]
    },
    {
      "data": "\u4eca\u5929\u5929\u6c14\u771f\u597d\u554a",
      "dataid": 27,
      "index": 2,
      "projectName": "xiedn_proj",
      "task": [
        {
          "aim": "",
          "choices": [
            "Positive",
            "Neutral",
            "Negative"
          ],
          "front": "option",
          "label": "",
          "mode": "single"
        }
      ]
    },
    {
      "data": "\u8bf7\u95ee\u6559\u5b66\u697c\u5728\u54ea",
      "dataid": 31,
      "index": 3,
      "projectName": "xiedn_proj",
      "task": [
        {
          "aim": "",
          "choices": [
            "Positive",
            "Neutral",
            "Negative"
          ],
          "front": "option",
          "label": "",
          "mode": "single"
        }
      ]
    },
    {
      "data": "\u8fd9\u4e2a\u83dc\u771f\u96be\u5403",
      "dataid": 29,
      "index": 4,
      "projectName": "xiedn_proj",
      "task": [
        {
          "aim": "",
          "choices": [
            "Positive",
            "Neutral",
            "Negative"
          ],
          "front": "option",
          "label": "",
          "mode": "single"
        }
      ]
    },
    {
      "data": "\u6211\u5b9e\u5728\u60f3\u4e0d\u51fa\u6765\u4e86",
      "dataid": 32,
      "index": 5,
      "projectName": "xiedn_proj",
      "task": [
        {
          "aim": "",
          "choices": [
            "Positive",
            "Neutral",
            "Negative"
          ],
          "front": "option",
          "label": "",
          "mode": "single"
        }
      ]
    }
  ]
}
                jsons = content['message']
                c = init_cnx()
                # Store label jsons in database

                c.close()
                session.pop('jsons', None)
                result = {"code": 0}
            else:
                result = {"code": 1, "message": "Session time out! Please apply for another 10 data!"}
        else:
            result = {"code": 1, "message": "Please login as users!"}
    else:
        result = {"code": 1, "message": "Please login first!"}
    return jsonify(result)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port="5000", debug=True, threaded=True)