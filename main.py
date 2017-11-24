# Currently this code assumes that the user will input correct information and does not check if the input is valid.
#pip install pymongo
from flask import Flask, render_template, request, redirect, url_for, session, escape
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient('mongodb://imran:password12345@ds113626.mlab.com:13626/profile-pal').get_database()
users = db.users
feedback_resume = db.Feedback_Resume
feedback_picture = db.Feedback_Picture

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['post', 'get'])
def login():
    if request.method=='POST':
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        credential = {'email':email,'password':password}
        if not users.find_one(credential):
            return 'Incorrect login credential. <a href="http://127.0.0.1:13000/">Go back.</a>'
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template("login.html")

@app.route('/signup', methods=['post', 'get'])
def signup():
    if request.method=='POST':
        name = request.form["name"].split()
        fname = name[0]
        lname = name[len(name) - 1]
        email = request.form["email"]
        password = request.form["password"]
        credential = {'email':email}
        if not users.find_one(credential):  
            credential = {'email':email,'password':password,'first_name':fname,'last_name':lname}
            db.users.insert_one(credential)
        else: return 'You have already signed up. <a href="http://127.0.0.1:13000/">Go back.</a>'
        session['email'] = email
        return redirect(url_for('dashboard'))
    return render_template('signup.html')

@app.route('/editProfile', methods=['post', 'get'])
def editprofile():
    if 'email' not in session: return '<a href="http://127.0.0.1:13000/">log in</a> first!' #requires an account to access this page
    if request.method=='POST':
        if 'confirm' in request.form:
            fname = request.form["firstName"]
            lname = request.form["lastName"]
            email = request.form["email"]
            confirmPassword = request.form["confirmPassword"]
            password = request.form["password"]
            credential = {'email':email}
            if password == confirmPassword and (email == session['email'] or not users.find_one(credential)):
                credential = {'email':email,'password':password,
                              'first_name':fname,'last_name':lname}
                users.find_one_and_update({'email': session['email']}, {'$inc': {'count': 1}, '$set':credential})
                return redirect(url_for('dashboard'))
    return render_template("profile2.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route("/profile")
def profile():
    if 'email' not in session: return '<a href="http://127.0.0.1:13000/">log in</a> first!' #requires an account to access this page
    return render_template("profile.html")

@app.route('/logout')
def logOut():
    session.pop('email', None)
    return 'You have logged out. <a href="http://127.0.0.1:13000/">Go back.</a>'

@app.route('/main', methods=['post', 'get'])
def main(email):
    if 'email' not in session: return 'log in first!'
    if request.method=='POST':
        if "del acc" in request.form:
            session.pop('email', None)
            #del users[email]
            return 'Account deleted. <a href="http://127.0.0.1:13000/">Go back.</a>'
        #other functionalities
        
    return render_template("profile2.html", user = email);

app.secret_key = 'A0Zr98j/3yX R~XXH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
