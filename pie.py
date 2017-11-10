from flask import Flask, render_template, request, redirect, url_for, session, escape

app = Flask(__name__)
users = {}

@app.route("/login/", methods=['post', 'get'])
def logIn():
    if request.method=='POST':
        username = request.form["username"]
        password = request.form["password"]

        if request.form["action"]=='signup':
            username = request.form["inputUsername"]
            password = request.form["inputPassword"]
            if username not in users:
                userData = [password,[],[]]
                users[username] = userData
            else: return 'You have already signed up.'
        else:
            if username not in users: return 'user name not found.'
            if password != users[username][0]: return 'password not correct.'
        session['username'] = request.form["username"]
        return redirect(url_for('home',username = request.form["username"]));
    return render_template("index.html");

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/main')
def main():
    return render_template("main.html")
@app.route('/logout/')
def logOut():
    session.pop('username', None)
    return 'You have logged out.'

@app.route('/user/<username>', methods=['post', 'get'])
def home(username):
    if 'username' not in session: return 'log in first!'
    if request.method=='POST':
        if "log out" in request.form:
            return redirect(url_for('logOut'))
        elif "del acc" in request.form:
            session.pop('username', None)
            del users[username]
            return 'Account deleted.'
        #other functionalities
        
    return render_template("main.html",user = username);

app.secret_key = 'A0Zr98j/3yX R~XXH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
