from flask import Flask, render_template, request, redirect, url_for, session, escape

app = Flask(__name__)
users = {}
session = {}

@app.route("/", methods=['post', 'get'])
def logIn():
    if request.method=='GET' and 'username' in session:
        return redirect(url_for('main',username = session['username']))
    elif request.method=='POST':
        if 'signup' in request.form:
            username = request.form["inputUsername"]
            password = request.form["inputPassword"]
            if username not in users:
                userData = [password,[],[]]
                users[username] = userData
            else: return 'You have already signed up. <a href="http://127.0.0.1:13000/">Go back.</a>'
        elif 'login' in request.form: 
            username = request.form["username"]
            password = request.form["password"]
            if username not in users: return 'user name not found. <a href="http://127.0.0.1:13000/">Go back.</a>'
            if password != users[username][0]: return 'password not correct. <a href="http://127.0.0.1:13000/">Go back.</a>'
        session['username'] = request.form["username"]
        return redirect(url_for('main',username = username));
    return render_template("index.html");

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/editprofile')
def editprofile():
    return render_template("editProfile.html")

@app.route('/logout/')
def logOut():
    session.pop('username', None)
    return 'You have logged out. <a href="http://127.0.0.1:13000/">Go back.</a>'

@app.route('/main')
def main():
    return redirect(url_for('index'))

@app.route('/main', methods=['post', 'get'])
def main(username):
    if 'username' not in session: return 'log in first!'
    if request.method=='POST':
        if "logout" in request.form:
            return redirect(url_for('index'))
        elif "del acc" in request.form:
            session.pop('username', None)
            del users[username]
            return 'Account deleted. <a href="http://127.0.0.1:13000/">Go back.</a>'
        #other functionalities
        
    return render_template("editProfile.html", user = username);

app.secret_key = 'A0Zr98j/3yX R~XXH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
