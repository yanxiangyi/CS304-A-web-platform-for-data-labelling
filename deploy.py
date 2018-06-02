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
ALLOWED_EXTENSIONS = set(['pdf', 'zip'])

app = Flask(__name__)
app.secret_key = 'any random string'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'any random string'
CORS(app)
cnx = connection.MySQLConnection(user='root',
                                 password='se2018',
                                 host='127.0.0.1',
                                 database='se_proj')
c = sql_conn(cnx)


@app.route("/")
@cross_origin()
def index_void():
    if 'email' in session:
        if session['level'] == 0:
            return render_template('index.html')
        elif session['level'] == 1:
            return render_template('index.html')
        else:
            return render_template('index.html')
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


@app.route("/index.html")
@cross_origin()
def index():
    if 'email' in session:
        if session['level'] == 0:
            return render_template('index.html')
        elif session['level'] == 1:
            return render_template('index.html')
        else:
            return render_template('index.html')
    return redirect(url_for('mainpage'))


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


@app.route("/imagelabel.html")
@cross_origin()
def imagelabel():
    return render_template('imagelabel.html')


@app.route("/textlabel.html")
@cross_origin()
def textlabel():
    return render_template('textlabel.html')


# @app.route("/textlabel2.html")
# @cross_origin()
# def textlabel2():
#     return render_template('textlabel2.html')


# @app.route('/email_current')
# @cross_origin()
# def email_current():
#     try:
#         email = session['email']
#         result = {'code': 0, 'message': email}
#         return jsonify(result)
#     except:
#         result = {'code': 1, 'message': "Please log in first!"}
#         return jsonify(result)


@app.route('/login_admin/email/<admin_email>/password/<pass_word>')
@cross_origin()
def email_login_admin(admin_email, pass_word):
    password = c.get_admin_passwd(admin_email=admin_email)
    if password is not None:
        if password == pass_word:
            result = {'code': 0}
            session['email'] = admin_email
            if c.get_admin_access_level(admin_email=admin_email) == 1:
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
    password = c.get_user_passwd(user_email=user_email)
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


# @app.route('/login/username/<user_name>/password/<pass_word>')
# @cross_origin()
# def username_login(user_name, pass_word):
#     password = c.get_user_passwd(username=user_name)
#     if password is not None:
#         if password == pass_word:
#             result = {'code': 0}
#         elif password != pass_word:
#             result = {'code': 1, 'message': 'Wrong password!'}
#     else:
#         result = {'code': 1, 'message': 'User doesn\'t exist!'}
#     return jsonify(result)


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


@app.route('/publish.html', methods=['GET', 'POST'])
@cross_origin()
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
            # root_path = os.path.join(EXTRACT_FOLDER, sourcename + "_" + datetime.datetime.today().strftime('%Y-%m-%d'))
            # os.renames(final_path, root_path)
            root_path = final_path
            admin_email = session['email']
            admin_id = c.get_admin_id(admin_email=admin_email)
            result = {"code": 0}
            insert = c.insert_source(sourcename=sourcename, finished=0, publisher=admin_id, description=description, publish_time=get_timestamp(), priority=1)
            if insert == -1:
                result = {"code": 1, "message": "Task insertion failed!"}
            else:
                load = c.load_data(root_path=root_path, sourcename=sourcename)
                if load == 0:
                    result = {"code": 1, "message": "Data insertion failed!"}
            return jsonify(result)
    return render_template('publish.html')


# @app.route('/test/<email>')
# @cross_origin()
# def test(email):
#     if session
#         return jsonify(result)

@app.route('/test')
@cross_origin()
def test():
    if 'email' in session:
        return jsonify(session.keys())
    else:
        return jsonify([])

@app.route('/profile')
@cross_origin()
def profile():
    if 'email' in session:
        email = session['email']
        if session['email'] != email:
            result = {"code": 1, "message": "Please login first!"}
            return jsonify(result)
        if session['level'] == 0:
            if c.user_exist(user_email=email):
                [user_id, user_email, user_name, password, signup_time, user_credit, num_answer, num_acc, num_val, num_val_tp] = c.get_user(user_email=email)
                user_num = c.get_user_number()
                result = {"user_id": user_id, "user_email": user_email,
                          "user_name": user_name, "user_credit": user_credit,
                          "num_acc": num_acc, "num_answer": num_answer,
                          "signup_time": signup_time, "num_val": num_val,
                          "num_val_tp": num_val_tp, "rank": 1-float(user_id)/float(user_num)}
                result = {"code": 0, "message": result}
            else:
                result = {"code": 1, "message": "User doesn\'t exist!"}
        else:
            [admin_id, admin_email, admin_name, password, level] = c.get_admin(admin_email=email)
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
    source_number = c.get_source_number()
    all_source = c.get_all_source()
    tasks = []
    for source in all_source:
        [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
        date = datetime.datetime.fromtimestamp(publish_date)
        task = {"publisher": publisher,
                "publish_date": str(date.month) + "." + str(date.day),
                "source_name": source_name,
                "if_finished": finished,
                "source_id": source_id,
                "description": description,
                "priority": priority,
                "number": num_json
        }
        tasks.append(task)
    result = {"code": 0,
              "message": {
                  "task_num": source_number,
                  "tasks": tasks[:5]
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
            source_number = c.get_source_number()
            all_source = c.get_all_source()
            tasks = []
            for source in all_source:
                [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
                task = {"publisher": publisher,
                        "publish_date": publish_date,
                        "source_name": source_name,
                        "if_finished": finished,
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
            all_source = c.get_all_source()
            tasks = []
            admin_email = session['email']
            for source in all_source:
                [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
                if publisher == c.get_admin_id(admin_email=admin_email):
                    task = {"publisher": publisher,
                            "publish_date": publish_date,
                            "source_name": source_name,
                            "if_finished": finished,
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
            source_number = c.get_source_number()
            all_source = c.get_all_source()
            tasks = []
            for source in all_source:
                [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
                task = {"publisher": publisher,
                        "publish_date": publish_date,
                        "source_name": source_name,
                        "if_finished": finished,
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

@app.route('/task1')
@cross_origin()
def task1():
    source_number = c.get_source_number()
    all_source = c.get_all_source()
    tasks = []
    for source in all_source:
        [source_id, source_name, finished, publisher, publish_date, description, priority, num_json] = source
        task = {"publisher": publisher,
                "publish_date": publish_date,
                "source_name": source_name,
                "if_finished": finished,
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
    return jsonify(result)
if __name__ == '__main__':
   app.run(host="0.0.0.0", port="5000", debug=True, threaded=True)
