# Currently this code assumes that the user will input correct information and does not check if the input is valid.
#pip install pymongo
import json
import os
import gridfs
import ResumeParser
import sentiment
import detect_face
from flask import Flask, render_template, request, redirect, url_for, session, escape
from pymongo import MongoClient
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) #where the user-uploaded files will be temporarily saved
user_photo = '\\static\\img\\photo.jpg' #where the user-uploaded photo will be saved
folder = '\\' #change to '\\' if windows, else '/'

app = Flask(__name__)
db = MongoClient('mongodb://imran:password12345@ds113626.mlab.com:13626/profile-pal').get_database()
users = db.users
feedback_resume = db.Feedback_Resume
feedback_picture = db.Feedback_Picture
fs=gridfs.GridFS(db)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




def analyzeRelease(Anger, Joy, Suprise, Blurred, Headwear):
    AngerHigh = "This image is not very professional. Our analysis of this profile photo shows that it is giving out a tone of anger. Try taking a picture with a smile!"
    AngerKHigh = "This image is ok, but it can be better and more professional. Our analysis of this profile phot shows that it is giving out some tones of anger. Retake the photo."
    SupriseHigh = "This is not an ideal image to utilize. Our analysis of this profile picture reveals that it seems the subject of the image is very surprised. Retake the photo with a more relaxed look."
    SupriseKHigh = "This image is ok, but it can definitely be improved. Our analysis of the profile picture shows that it is giving off some tones of surprise. We suggest you take another image and look a but more relaxed, perhaps just give a little smile."
    GoodImage = "Wow, you look like you are ready to start working today. Our analysis reveals that this is a very good image to utilize for any professional profile."
    HeadwearLikely = "TAKE OFF THAT HAT.The analysis of your profile picture shows you are wearing some type of head garment.If it is for a non religious reason, take it off and retake your picture."
    BlurredLikely = "Our analysis of your profile picture shows that the image is somewhat blurrred. We suggest retaking the picture and making sure the camera is still so you get a clearer image."
    if(Blurred==('LIKELY' or 'VERY_LIKELY')):
        return  HeadwearLikely
    elif(Headwear==('LIKELY' or 'VERY_LIKELY')):
        return BlurredLikely
    elif(Anger == 'VERY_LIKELY'):
        return AngerHigh
    elif(Anger == "LIKELY"):
        return AngerKHigh
    elif(Suprise == 'VERY_LIKELY'):
        return SupriseHigh
    elif(Suprise =="LIKELY"):
        return SupriseKHigh
    else: return GoodImage

def analyzeResume(score):
    VeryLowScore = "Your writing is extremely negative and needs to include more positive words."
    LowScore = "The general trend of your writing is negative there are slight improvements that you can make"
    HighScore ="Overall a positive trend in writing. further positive structures and phrases can be included but good job regardless."
    VeryHighScore = "Excellent and positive writing. Keep up the good work."

    if score < -0.5:
        return VeryLowScore
    elif score < 0 and score >= -0.5:
        return LowScore
    elif score >0 and score <=0.5:
        return HighScore
    else:
        return VeryHighScore

@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['post', 'get'])
def login():
    error = None

    if request.method=='POST' and request.form["inputEmail"]!='' and request.form["inputPassword"] !='':
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        credential = {'email':email,'password':password}
        if not users.find_one(credential):
            error = "Invalid Credentials"
        else:
            session['email'] = email
            return redirect(url_for('dashboard'))
    return render_template("login.html",error=error)

@app.route('/signup', methods=['post', 'get'])
def signup():
    error =None
    success=None
    if request.method=='POST' and request.form["password"]!='' and request.form["email"] !='' and request.form["name"]!='':
        name = request.form["name"].split()
        fname = name[0]
        lname = name[len(name) - 1]
        email = request.form["email"]
        password = request.form["password"]
        credential = {'email':email}

        if not users.find_one(credential):  
            credential = {'email':email,'password':password,'first_name':fname,'last_name':lname,'image':'', 'resume':''}

            db.users.insert_one(credential)
            success="Success"
        else:
            error = "Invalid"
    return render_template('signup.html',error=error,success=success)

@app.route('/editProfile', methods=['post', 'get'])
def editprofile():
    if 'email' not in session: return redirect(url_for('login'))#requires an account to access this page
    flag = 0 # 0: no error, 1: password and confirm password not the same, 2: the new email is already associated with an account
    imageFlag = 0 # 0: no uploaded photo, 1: user has previously uploaded a photo
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
                session['email'] = email
                return redirect(url_for('profile'))
            elif password != confirmPassword:
                flag = 1
            elif email != session['email'] and users.find_one(credential):
                flag = 2
        if 'file' in request.form:
            file = request.files['resume']
            photo = request.files['photo']
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                parsed = ResumeParser.parseResume(filename, UPLOAD_FOLDER+folder+filename)
                users.find_one_and_update({'email': session['email']}, {'$inc': {'count': 1}, '$set':{'resume':parsed}})
                os.remove(UPLOAD_FOLDER+folder+filename)
            if photo:
                filename = secure_filename(photo.filename)
                file_id = fs.put(photo,filename=filename)
                data={'image':file_id}
                users.find_one_and_update({'email': session['email']}, {'$inc': {'count': 1}, '$set':data})
    user_info = users.find_one({'email':session['email']})
    if fs.exists(user_info['image']):
        imageFlag = 1
        image_data = fs.get(user_info['image'])
        f = open(UPLOAD_FOLDER + user_photo, 'wb')
        f.write(image_data.read())
        f.close()
    elif os.path.isfile(UPLOAD_FOLDER + user_photo):
        os.remove(UPLOAD_FOLDER + user_photo)
#example format for user_info:
#{'email': 'ia761@nyu.edu', 'resume': 'resume', 'last_name': 'Ahmed', 'image': ObjectId('5a19230f7c051e1a6c474c67'), 'first_name': 'Imran', 'password': 'pass'}
    return render_template("profile2.html", flag = flag, user_info = user_info, imgFlag = imageFlag)

@app.route('/dashboard', methods=['post', 'get'])
def dashboard():
    if 'email' not in session: return redirect(url_for('login'))#requires an account to access this page
    resume = True
    photo = True
    emotions = False
    photo_feedback = False
    resume_feedback = False
    score = False
    error = False
    if request.method=='POST':
        user_info = users.find_one({'email':session['email']})
        if 'resume' in request.form:
            if user_info['resume'] != '':
                resume_data = user_info['resume']
                fh = open("sentiment_results.txt", 'w')
                parsed_output = json.loads(resume_data)
                fh.write(json.dumps(parsed_output["DocumentElement"]["Resume"]["Experience"], indent=4, sort_keys=True))
                fh.close()
                results = sentiment.analyze("sentiment_results.txt")
                score = results[0]
                resume_feedback = analyzeResume(score)
            else:
                resume=False
        if 'photo' in request.form:
            if fs.exists(user_info['image']):
                image_data = fs.get(user_info['image'])
                f = open(UPLOAD_FOLDER + user_photo, 'wb')
                f.write(image_data.read())
                f.close()
                emotions = detect_face.detect_faces(UPLOAD_FOLDER + user_photo)
                photo_feedback = analyzeRelease(emotions["anger"], emotions["joy"], emotions["surprise"],emotions["blurred"],emotions["headwear"]) if emotions else False
                error = False if photo_feedback else True

            else:
                photo = False
    return render_template("dashboard.html",emotions=emotions,photo=photo, score=score, resume=resume,photo_feedback=photo_feedback, resume_feedback=resume_feedback, error=error)

@app.route("/profile")
def profile():
    imageFlag = 0 # 0: no uploaded photo, 1: user has previously uploaded a photo
    if 'email' not in session: return redirect(url_for('login')) #requires an account to access this page
    user_info = users.find_one({'email':session['email']})
    if fs.exists(user_info['image']):
        imageFlag = 1
        image_data = fs.get(user_info['image'])
        f = open(UPLOAD_FOLDER + user_photo, 'wb')
        f.write(image_data.read())
        f.close()
    elif os.path.isfile(UPLOAD_FOLDER + user_photo):
        os.remove(UPLOAD_FOLDER + user_photo)
    return render_template("profile.html", user_info = user_info, imgFlag = imageFlag)

@app.route('/logout')
def logOut():
    if os.path.isfile(UPLOAD_FOLDER + user_photo):
        os.remove(UPLOAD_FOLDER + user_photo)
    session.pop('email', None)
    return redirect(url_for("login"))


app.secret_key = 'A0Zr98j/3yX R~XXH!jN]LWX/,?RT'
app.run("127.0.0.1", 13000, debug=True)
