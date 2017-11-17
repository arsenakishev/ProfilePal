from flask import Flask, render_template, request, redirect, url_for, session, escape

app = Flask(__name__)
users = {}  # temporary placeholder for a database

@app.route('/')
def index():
    if 'email' in session:
        return render_template("profile2.html")
    return redirect(url_for('login'))

@app.route('/login', methods=['post', 'get'])
def login():
    if request.method=='POST':
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        if email not in users: return 'This email is not associated with any account. <a href="http://127.0.0.1:13000/">Go back.</a>'
        if password != users[email][0]: return 'password not correct. <a href="http://127.0.0.1:13000/">Go back.</a>'
        session['email'] = email
        return redirect(url_for('editprofile'))
    return render_template("login.html")

@app.route('/signup', methods=['post', 'get'])
def signup():
    if request.method=='POST':
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        if email not in users:
            userData = [password,[],[]]
            users[email] = userData
        else: return 'You have already signed up. <a href="http://127.0.0.1:13000/">Go back.</a>'
        session['email'] = email
        return redirect(url_for('editprofile'))
    return render_template('signup.html')

@app.route('/editProfile')
def editprofile():
    return render_template("profile2.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route('/logout/')
def logOut():
    session.pop('email', None)
    return 'You have logged out. <a href="http://127.0.0.1:13000/">Go back.</a>'

@app.route('/main', methods=['post', 'get'])
def main(email):
    if 'email' not in session: return 'log in first!'
    if request.method=='POST':
        if "logout" in request.form:
            return redirect(url_for('index'))
        elif "del acc" in request.form:
            session.pop('email', None)
            del users[email]
            return 'Account deleted. <a href="http://127.0.0.1:13000/">Go back.</a>'
        #other functionalities
        
    return render_template("profile2.html", user = email);

app.secret_key = 'A0Zr98j/3yX R~XXH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
