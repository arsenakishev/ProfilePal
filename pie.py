from flask import Flask, render_template, request, redirect, url_for, session, escape

app = Flask(__name__)
users = {}

@app.route("/login/", methods=['post', 'get'])
def logIn():
    if request.method=='POST':
        users["test"] = ["123",[],[]]
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

@app.route('/')
@app.route('/index')
def index():
    return render_template("login.html")

@app.route('/action/',methods=['post'])
def action():
    if request.method=="POST":
        if request.form["action"] =='signup':
            return render_template("signup.html")
    return render_template("login.html")
@app.route('/editprofile')
def editprofile():
    return render_template("editProfile.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/logout/')
def logOut():
    session.pop('username', None)
    return 'You have logged out.'

@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/user/<username>', methods=['post', 'get'])
def home(username):
    if 'username' not in session: return 'log in first!'
    if request.method=='POST':
        if "logout" in request.form:
            return redirect(url_for('index'))
        elif "del acc" in request.form:
            session.pop('username', None)
            del users[username]
            return 'Account deleted.'
        #other functionalities
        
    return render_template("editProfile.html", user = username);

app.secret_key = 'A0Zr98j/3yX R~XXH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
