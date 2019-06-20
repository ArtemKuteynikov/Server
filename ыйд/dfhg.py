#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import json
import json
from email.mime.text import MIMEText
from flask import render_template, request
import sqlite3
from werkzeug import generate_password_hash, check_password_hash
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext import admin
from flask.ext.admin.contrib import sqla
from flask.ext.admin import expose
import smtplib
import random
import socket


socket.gethostbyname(socket.gethostname())
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
ip = str(s.getsockname()[0])
s.close()

app = Flask(__name__)

@app.route('/')
def main():
    projectpath2 = ''
    return render_template('gfdj.html')

@app.route('/signUp', methods=['POST', 'GET'])
def signUp():
    try:
        projectpath = request.values['projectFilepath']
        projectpath0 = request.values['projectFilepath1']
        projectpath01 = request.values['projectFilepath2']
        projectpath03 = request.values['projectFilepath3']
        projectpath04 = request.values['projectFilepath4']
        projectpath05 = request.values['projectFilepath5']
        conn = sqlite3.connect("mydatabaseq1.db")  # или :memory: чтобы сохранить в RAM
        cursor = conn.cursor()
        if projectpath != "" and projectpath0 != "" and projectpath01 != "":
            print(projectpath0)
            if projectpath01 == projectpath0:
                print(projectpath)
                projectpath1 = generate_password_hash(projectpath0)


                cursor.execute("INSERT INTO albums7 (title, pass, E_mail, Name, Surname) VALUES ('{}', '{}', '{}', '{}', '{}')".format(projectpath, projectpath1, projectpath03, projectpath04, projectpath05))
                conn.commit()
                data = cursor.fetchall()

                if len(data) is 0:
                    conn.commit()
                    return render_template('ghy.html')
                else:
                    error = str(data[0])
                    return render_template('gfdj.html', error = error)
                    #return json.dumps({'error': str(data[0])})
            else:
                error = "Different values for 'Password' and 'Repeat password'"
                return render_template('gfdj.html', error=error)
        else:
            error = "Enter the required fields"
            return render_template('gfdj.html', error=error)

    except Exception as e:
        error = str(e)
        return render_template('gfdj.html', error=error)
    finally:
        cursor.close()
        conn.close()

@app.route('/showSignUp')
def showSignIn():
    return render_template('ghy.html')

@app.route('/signIn', methods=['POST', 'GET'])
def signIn():
    try:
        global projectpath2
        projectpath2 = request.values['projectFilepath2']
        projectpath02 = request.values['projectFilepath3']
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        sql = "SELECT pass FROM albums7 WHERE title=('{}')".format(projectpath2)
        sql3 = "SELECT Name, Surname FROM albums7 WHERE title=('{}')".format(projectpath2)
        cursor1.execute(sql)
        sql1 = cursor1.fetchone()
        cursor1.execute(sql3)
        sql5 = cursor1.fetchone()
        print(sql1[0], projectpath02)
        print(type(sql1[0]), type(projectpath02))
        sql10 = str(sql1[0])
        sql50 = str(sql5[0])+' '+str(sql5[1])
        if projectpath2 == 'admin1' or projectpath2 == 'admin2':
            if check_password_hash(sql10, projectpath02) == True:
                return render_template('ggga.html', user = sql50)

            else:
                error = "Incorrect Login or Password"
                return render_template('ghy.html', error=error)
        else:
            if check_password_hash(sql10, projectpath02) == True:
                return render_template('ggg.html', user = sql50)

            else:
                error = "Incorrect Login or Password"
                return render_template('ghy.html', error=error)
    except Exception as e:
        error = str(e)
        return render_template('ghy.html', error=error)
    finally:
        cursor1.close()
        conn.close()
app.config['SECRET_KEY'] = '123456790'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabaseq1.db'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

@app.route('/Admin')
def Admin():
    return '<a href="/admin/">Click me to get to Admin!</a>'


class Users(db.Model):
    __tablename__ = 'albums7'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    E_mail = db.Column(db.String(100))
    Name = db.Column(db.String(100))
    Surname = db.Column(db.String(100))
    block = db.Column(db.Integer)

    def __unicode__(self):
        return self.desc

class GoHome(db.Model):
    __tablename__ = 'albums6'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class CarAdmin(sqla.ModelView):
    column_display_pk = True
    form_columns = ['id', 'title', 'E_mail', 'Name', 'Surname', 'block']
    column_searchable_list = ('title',)

class CarAdmin1(sqla.ModelView):

    @expose('/')
    def index(self):
        return self.render('ggga.html')



admin = admin.Admin(app, name='Admin')

admin.add_view(CarAdmin(Users, db.session))
admin.add_view(CarAdmin1(GoHome, db.session))

@app.route('/ShowRes_pass')
def ShowRes_pass():
    return render_template('ggg1.html')

@app.route('/Res_pass', methods=['POST', 'GET'])
def Res_pass():
    try:
        global log
        log = request.values['projectFilepath9']
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor1 = conn.cursor()
        sql9 = "SELECT E_mail FROM albums7 WHERE title=('{}')".format(log)
        cursor1.execute(sql9)
        adr = cursor1.fetchone()
        adr = str(adr[0])
        print(adr)
        global txtparam
        MAIL_SERVER = 'smtp.gmail.com'
        MAIL_PORT = 465

        print('Авторизация:')

        MAIL_USERNAME = 'kuteynikov.artyom@gmail.com'
        MAIL_PASSWORD = 'nayda2002'

        FROM = MAIL_USERNAME
        TO = adr
        txtparam = str(random.randint(100001, 999999))
        # теперь можно использовать кириллицу
        msg = 'Ваш код сброа пароля:{}. Если вы не запрашивали сброс пароля, удалите это сообшение и никому не сообщайте код.'.format(txtparam)
        msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')

        smtpObj = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
        smtpObj.ehlo()
        smtpObj.login(MAIL_USERNAME, MAIL_PASSWORD)

        smtpObj.sendmail(FROM, TO,
                         'Subject: Сброс пароля. \n{}'.format(msg).encode('utf-8'))
        smtpObj.quit()
        print('письмо отправлено')
        return render_template('ggg2.html')
    except Exception as e:
        error = str(e)
        return render_template('ggg1.html', error=error)
    finally:
        cursor1.close()
        conn.close()

@app.route('/Check_code', methods=['POST', 'GET'])
def Check_code():
    projectpath2 = request.values['projectFilepath']
    if projectpath2 == txtparam:
        return render_template('ghy1.html')
    else:
        error = "Incorrect code"
        return render_template('ggg2.html', error=error)

@app.route('/Upd_pass', methods=['POST', 'GET'])
def Upd_pass():
    try:
        projectpath2 = request.values['projectFilepath2']
        projectpath02 = request.values['projectFilepath3']
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor2 = conn.cursor()
        if projectpath2 == projectpath02:
            projectpath12 = generate_password_hash(projectpath02)
            sql = "UPDATE albums7 SET pass=('{}') WHERE title=('{}')".format(projectpath12, log)
            cursor2.execute(sql)
            conn.commit()
        else:
            error = "Password isn't equal to repeated password"
            return render_template('ghy1.html', error = error)
        print(projectpath02)
        return render_template('ghy.html')
    except Exception as e:
        error = str(e)
        return render_template('ghy.html', error=error)
    finally:
        cursor2.close()
        conn.close()

@app.route('/Show_info', methods=['POST', 'GET'])
def Show_info():
    sql = "SELECT Name, Surname, E_mail FROM albums7 WHERE title=('{}')".format(projectpath2)
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor1 = conn.cursor()
    cursor1.execute(sql)
    sql1 = cursor1.fetchone()
    sql3 = str(sql1[0])
    sql4 = str(sql1[1])
    sql5 = str(sql1[2])
    sql6 = projectpath2
    cursor1.close()
    conn.close()
    return render_template('pro.html', user1 = sql3, user2 = sql4, user3 = sql5, user4 = sql6)

@app.route('/ch_info1', methods=['POST', 'GET'])
def ch_info1():
    sql = "SELECT Name, Surname, E_mail FROM albums7 WHERE title=('{}')".format(projectpath2)
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor1 = conn.cursor()
    cursor1.execute(sql)
    sql1 = cursor1.fetchone()
    sql3 = str(sql1[0])
    sql4 = str(sql1[1])
    sql5 = str(sql1[2])
    sql6 = projectpath2
    cursor1.close()
    conn.close()
    return render_template('gfdj1.html', user1 = sql3, user2 = sql4, user3 = sql5, user4 = sql6)

@app.route('/ch_info2', methods=['POST', 'GET'])
def ch_info2():
    projectpath05 = request.values['projectFilepath']
    projectpath04 = request.values['projectFilepath3']
    projectpath = request.values['projectFilepath4']
    projectpath03 = request.values['projectFilepath5']
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor2 = conn.cursor()
    if projectpath != '':
        sql = "UPDATE albums7 SET Name=('{}') WHERE title=('{}')".format(projectpath, projectpath2)
        cursor2.execute(sql)
        conn.commit()
    if projectpath03 != '':
        sql = "UPDATE albums7 SET Surname=('{}') WHERE title=('{}')".format(projectpath03, projectpath2)
        cursor2.execute(sql)
        conn.commit()
    if projectpath04 != '':
        sql = "UPDATE albums7 SET E_mail=('{}') WHERE title=('{}')".format(projectpath04, projectpath2)
        cursor2.execute(sql)
        conn.commit()
    if projectpath05 != '':
        sql = "UPDATE albums7 SET title=('{}') WHERE title=('{}')".format(projectpath05, projectpath2)
        cursor2.execute(sql)
        conn.commit()
    cursor2.close()
    conn.close()
    return render_template('pro1.html')

@app.route('/MyPage', methods=['POST', 'GET'])
def MyPage():
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor1 = conn.cursor()
    sql3 = "SELECT Name, Surname FROM albums7 WHERE title=('{}')".format(projectpath2)
    cursor1.execute(sql3)
    sql5 = cursor1.fetchone()
    sql50 = str(sql5[0]) + ' ' + str(sql5[1])
    if projectpath2 == 'admin1' or projectpath2 == 'admin2':
        return render_template('ggga.html', user=sql50, admin=admin)
    else:
        return render_template('ggg.html', user=sql50)

@app.route('/Ch_pass1', methods=['POST', 'GET'])
def Ch_pass1():
    return render_template('Ch_pass.html')

@app.route('/Ch_pass2', methods=['POST', 'GET'])
def Ch_pass2():
    projectpath1 = request.values['projectFilepath2']
    projectpath02 = request.values['projectFilepath3']
    projectpath3 = request.values['projectFilepath4']
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor1 = conn.cursor()
    sql3 = "SELECT pass FROM albums7 WHERE title=('{}')".format(projectpath2)
    cursor1.execute(sql3)
    sql5 = cursor1.fetchone()
    sql50 = str(sql5[0])
    if check_password_hash(sql50, projectpath1) == True:
        if projectpath02 == projectpath3:
            projectpath12 = generate_password_hash(projectpath02)
            sql = "UPDATE albums7 SET pass=('{}') WHERE title=('{}')".format(projectpath12, projectpath2)
            cursor1.execute(sql)
            conn.commit()
            return render_template('nnn.html')
        else:
            error = 'Different values for new password and repeat password'
            return render_template('Ch_pass.html', error = error)
    else:
        error = 'Incorrect old password'
        return render_template('Ch_pass.html', error = error)

@app.route('/ConTS', methods=['POST', 'GET'])
def ConTS():
    try:
        a = 1
        posts = []
        conn = sqlite3.connect("mydatabaseq1.db")
        cursor = conn.cursor()
        cursor.execute("SELECT title FROM albums6")
        sql = cursor.fetchall()
        for row in sql:
            cursor.execute("SELECT title, Post FROM albums6 WHERE id = ('{}')".format(a))
            sql1 = cursor.fetchone()
            posts.append({
                'author': {'nickname': str(sql1[0])},
                'body': str(sql1[1])
            })
            a+=1
        return render_template('techsup.html', posts = posts)
    except Exception as e:
        error = str(e)
        return render_template('techsup.html', error=error)
    finally:
        cursor.close()
        conn.close()

@app.route('/ConTS1', methods=['POST', 'GET'])
def ConTS1():
    conn = sqlite3.connect("mydatabaseq1.db")
    cursor = conn.cursor()
    cursor.execute("SELECT block FROM albums7 WHERE title = ('{}')".format(projectpath2))
    sql1 = cursor.fetchone()
    sql11 = sql1[0]
    if sql11 == 0:
        posts = []
        a = 1
        projectpath = request.values['projectFilepath2']

        cursor.execute("INSERT INTO albums6 (title, Post) VALUES ('{}', '{}')".format(projectpath2, projectpath))
        conn.commit()
        cursor.execute("SELECT title FROM albums6")
        sql = cursor.fetchall()
        for row in sql:
            cursor.execute("SELECT title, Post FROM albums6 WHERE id = ({})".format(a))
            sql1 = cursor.fetchone()
            posts.append({
                'author': {'nickname': str(sql1[0])},
                'body': str(sql1[1])
            })
            a+=1
        cursor.close()
        conn.close()
        return render_template('techsup.html', posts = posts)
    else:
        error = 'Chat had been blocked for you'
        return render_template('techsup.html', error=error)

@app.route('/FagLog', methods=['POST', 'GET'])
def FagLog():
    error = 'Да иди ты нафиг, регестрируйся заново, мне тебя как искать, по запаху!?'
    return render_template('gfdj.html', error = error)

@app.route('/cours')
def cours():
    return render_template('course.html')

@app.route('/ShowTasks')
def ShowTasks():
    return render_template('tasks.html')

@app.route('/ShowTheory')
def ShowTheory():
    return render_template('course.html')

@app.route('/AboutCourse')
def AboutCourse():
    return render_template('course.html')

@app.route('/Task1')
def Task1():
    return render_template('уч.html')

@app.route('/addshare2', methods=['POST', 'GET'])
def addshare2():
    global selected
    post = request.args.get('post', 0, type=int)
    print(post)
    return json.dumps({'selected post': str(post)})

app.run(host = ip, port=5000, debug = False)