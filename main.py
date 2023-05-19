from flask import Flask, render_template, Response,  request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import sys
import cv2
import subprocess
from IPython.display import IFrame

#for running detect.py
from detect import get_pose_model,get_pose,prepare_vid_out,prepare_image,fall_detection,falling_alarm
from tqdm import tqdm
import time

sys.path.append('../utils')
app = Flask(__name__,template_folder='template')

#process of connection database
app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] ='localhost'
app.config['MYSQL_USER'] ='root'
app.config['MYSQL_PASSWORD'] ='swagatoghosh@123'
app.config['MYSQL_DB'] ='geeklogin'

mysql = MySQL(app)

#login purpose
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            #session['id'] = account['id']
            session['username'] = account['username']
            session['password'] = account['password']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg = msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template('register.html', msg = msg)

#signup purpose: for new user
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        print(cursor.Error)
        print(cursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s)', (username, password, email, ))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('home.html', msg = msg)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/reg')
def reg():
    return render_template('register.html')
    
    
@app.route('/my')
def mylink():
    #file = open(r'G:\My Drive\Final year project\Human-Fall-Detection using YoloV7 Pose estimation model 2','r').read()
    #file = open('C:\\Users\\Acer\\PycharmProjects\\Flask\\detect.py','r').read()
    #exec(file)
    subprocess.run("python detect2.py --source 0")

    #return subprocess.run("python detect2.py --source 0")
    #IFrame(subprocess.run("python detect2.py --source 0"), width='50%', height=350)

#subprocess helps to run command line argument. here subprocess running detect1.py --source 0

# @app.route('/my')
# def index():
#     return render_template('camera.html')
#
# @app.route('/video_feed')
# def video_feed():
#     return Response(subprocess.run("python detect2.py --source 0"), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__== "__main__":
    app.run(debug=True, port=8000)
