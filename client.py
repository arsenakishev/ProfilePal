from flask import Flask, render_template, request, redirect, url_for, session, escape
import socket
import time
import datetime
import uuid

app = Flask(__name__)
host = "hs2685@code.engineering.nyu.edu" #replace with the address you are connecting to
port = 9001    #replace with the port you are using
buff = 8192
s = socket.socket()

@app.route("/", methods=['post', 'get'])
def logIn():
    if 'username' in session: return redirect(url_for('home',username = session['username']))
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]
        if password == '' or username == '': return 'Do not leave any field blank. <a href="http://127.0.0.1:13000/">Retry</a>'
        if '\n' in password or '\n' in username: return 'Password and username cannot contain "\n". <a href="http://127.0.0.1:13000/">Retry</a>'
        s.connect((host, port))
        uid = uuid.uuid1().hex  #unique identifier
        if request.form["action"]=='signUp': #sign up
            msg = uid + 'SU' + username + '\n' + password
            s.send(msg)
            response = s.recv(buff)
            while uid not in response:
                response = s.recv(buff)
            s.close()
            if response == uid + 'f':
                return 'Username already in use.<a href="http://127.0.0.1:13000/">Try again</a>.'
        else:   #log in
            s.send(uid + 'LI' + username + '\n' + password)
            response = s.recv(buff)
            while uid not in response:
                response = s.recv(buff)
            s.close()
            if response == uid + '0':
                return 'username not found. <a href="http://127.0.0.1:13000/">Retry</a>'
            if response == uid + '2': return 'password not correct. <a href="http://127.0.0.1:13000/">Retry</a>'
        session['username'] = request.form["username"]
        return redirect(url_for('home',username = request.form["username"]));
    return render_template("login.html");

@app.route('/user/<username>', methods=['post', 'get'])
def home(username):
    if 'username' not in session or username != session['username']: return '<a href="http://127.0.0.1:13000/">log in</a> first!'
    if request.method=='POST':
        uid = uuid.uuid1().hex
        if "log out" in request.form:
            session.pop('username', None)
            return redirect(url_for('logIn'))
        elif "del acc" in request.form: #delete account
            session.pop('username', None)
            s.send(uid + 'DA' + username)
            time.sleep(1) #make sure that any future requests will arrive at the back end servers later than this request
            s.close()
            return redirect(url_for('logIn'))
        
        #rest of the functions on the main page here




        
    return render_template("main.html",user = username);

app.secret_key = 'A0Zr98j/3yX R~XxH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
