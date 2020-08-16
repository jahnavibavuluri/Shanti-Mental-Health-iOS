from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import random, copy
import sqlite3
import datetime
from datetime import date
from sqlite3 import Error
import uuid
from flask_mail import Mail, Message
import hashlib
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'shantimentalhealthapp@gmail.com'
app.config['MAIL_PASSWORD'] = 'shanti2020'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
db = SQLAlchemy(app)
mail = Mail(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(80))
    profile = db.relationship('UserProfile', backref='user')
    stats = db.relationship('Stats', backref='user')
    rmchange = db.relationship('rmchange', backref='user')
    rmpast = db.relationship('rmpast', backref='user')
    pwcontrol = db.relationship('pwcontrol', backref='user')
    pwevidence = db.relationship('pwevidence', backref='user')
    nttrue = db.relationship('nttrue', backref='user')
    ntpositive = db.relationship('ntpositive', backref='user')
    scgood = db.relationship('scgood', backref='user')
    screword = db.relationship('screword', backref='user')
    scchange = db.relationship('scchange', backref='user')
    dmworst = db.relationship('dmworst', backref='user')

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    sex = db.Column(db.String(50))
    hobbies = db.Column(db.Text)
    interests = db.Column(db.Text)
    imp = db.Column(db.Text)

class Stats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.String(20)) #db.DateTime, default=datetime.datetime.now().date())
    overall = db.Column(db.Integer)
    rm = db.Column(db.Integer)
    pw = db.Column(db.Integer)
    nt = db.Column(db.Integer)
    sc = db.Column(db.Integer)
    dm = db.Column(db.Integer)
    c = db.Column(db.Integer)
    el = db.Column(db.Integer)
    s = db.Column(db.Integer)

class rmchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class rmpast(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    add =db.Column(db.Boolean, default=False)

class pwcontrol(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class pwevidence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class nttrue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class ntpositive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=True)

class scgood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    add = db.Column(db.Boolean, default=True)

class screword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class scchange(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    control = db.Column(db.Boolean, default=False)
    add = db.Column(db.Boolean, default=True)

class dmworst(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class dmnow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime, default=datetime.datetime.now().date())
    thought = db.Column(db.Text)
    suggestion = db.Column(db.Text)
    add = db.Column(db.Boolean, default=False)

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        hashed_password = hashlib.sha256(request.json["password"].encode()).hexdigest()
        username = request.json["username"]
        email = request.json["email"]
        if (User.query.filter_by(username=username).first() is None) and (User.query.filter_by(email=email).first() is None):
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        #return "success"
            return "success"
        return "user or email exists"
    else:
        return current_user.username

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.json["username"]
        user = User.query.filter_by(username=username).first()
        if user:
            password = hashlib.sha256(request.json["password"].encode()).hexdigest()
            if (password == user.password):
                login_user(user)
                return current_user.username
                #return "match"
            return "invalid password"
    return "no user"

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return "logged out"

@app.route('/whoisloggedin', methods=["GET"])
def whoisloggedin():
    if current_user:
        return str(current_user.username)
    else:
        return "no user"


@app.route('/initialuserprofile', methods=["GET", "POST"])
def initialuserprofile():
    if request.method == "POST":
        first_name = request.json["firstname"]
        last_name = request.json["lastname"]
        age = request.json["age"]
        gender = request.json["gender"]
        hobbies = request.json["hobbies"]
        interests = request.json["interests"]
        importantpeople = request.json["importantpeople"]
        new_user_profile = UserProfile(user_id=current_user.id, first_name=first_name,\
        last_name=last_name, age=age, sex=gender,hobbies=hobbies,interests=interests,\
        imp=importantpeople)
        db.session.add(new_user_profile)
        db.session.commit()
        return "success"
    else:
        user = UserProfile.query.filter_by(user_id=current_user.id).first()
        dict = {
            "username":current_user.username,
            "firstName":user.first_name,
            "lastName":user.last_name,
            "age":user.age,
            "sex":user.sex,
            "hobbies":user.hobbies,
            "interests":user.interests,
        }
        return dict


@app.route('/editprofile', methods=["POST"])
def editprofile():
    first_name = request.json["firstname"]
    last_name = request.json["lastname"]
    age = request.json["age"]
    gender = request.json["gender"]
    hobbies = request.json["hobbies"]
    interests = request.json["interests"]
    user = UserProfile.query.filter_by(user_id=current_user.id).first()
    user.first_name = first_name
    user.last_name = last_name
    user.age = age
    user.sex = gender
    user.hobbies = hobbies
    user.interests = interests
    db.session.commit()
    return "success"

@app.route('/atleastonequiz', methods = ["GET"])
def atleastonequiz():
    user = current_user.id
    quizArray = Stats.query.filter_by(user_id=user).all()
    if (len(quizArray)>0):
        return "at least one"
    else:
        return "no quizzes"


@app.route('/quizstat', methods = ["GET"])
@login_required
def quizstat():
    userid = current_user.id
    last_quiz = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).first()
    dict = {
        "overall":last_quiz.overall,
        "rm":last_quiz.rm,
        "pw":last_quiz.pw,
        "nt":last_quiz.nt,
        "sc":last_quiz.sc,
        "dm":last_quiz.dm,
        "s":last_quiz.s,
        "el":last_quiz.el,
        "c":last_quiz.c
    }
    print(last_quiz)
    return dict

@app.route('/statsmessage', methods = ["GET"])
@login_required
def statsmessage():
    userid = current_user.id
    latest_quiz = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).first()

    first = ""

    overall = latest_quiz.overall
    positive_overall = 100-overall

    if (positive_overall > 80):
        first = "You’re making great progress! Your stats show great improvement, keep smiling and being happy! Remember, the key to keeping this progress is to clear your mind and keep your thoughts organized. An organized mind is a healthy mind! "
    elif (positive_overall > 50):
        first = "You’re in great shape! There is a good amount of progress that keeps you on the way to a healthier mind! Keep logging your thoughts and doing the recommended activities for healthier thoughts. You’re doing well! "
    elif (positive_overall > 30):
        first = "Slow progress is still some progress! Baby steps! Always keep in mind that getting to a healthier mindset takes time and practice. It’s about changing the way you think and how those thoughts affect you. "
    else:
        first = "Hmmmmm, looks like there hasn’t been much progress and your overall mental health seems to be low. Don’t let this get you down - there is still so much we can do! Keep a positive mindset and set goals so you can continously work towards them. And most importantly, don't give up!"

    return first

@app.route('/progressmessage', methods = ["GET"])
@login_required
def progressmessage():
    weekly_quizzes = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=current_user.id).limit(7).all()
    #print(weekly_quizzes)
    weekly_quizzes.reverse()
    #print(weekly_quizzes)
    #max = 0
    #max2 = 0
    message = ""
    rm_avg = 0
    pw_avg = 0
    nt_avg = 0
    sc_avg = 0
    dm_avg = 0
    c_avg = 0
    e_avg = 0
    s_avg = 0

    for i in weekly_quizzes:
        rm_avg += i.rm
        pw_avg += i.pw
        nt_avg += i.nt
        sc_avg += i.sc
        dm_avg += i.dm
        c_avg += i.c
        e_avg += i.el
        s_avg += i.s


    rm_avg /= len(weekly_quizzes)
    pw_avg /= len(weekly_quizzes)
    nt_avg /= len(weekly_quizzes)
    sc_avg /= len(weekly_quizzes)
    dm_avg /= len(weekly_quizzes)
    c_avg /= len(weekly_quizzes)
    e_avg /= len(weekly_quizzes)
    s_avg /= len(weekly_quizzes)

    max1 = max(rm_avg, pw_avg, nt_avg, sc_avg, dm_avg)
    max2 = max(c_avg, e_avg, s_avg)

    if (max1 == rm_avg):
        message += "Looks like your rumination is what needs to be tackled this week. To fight rumination, identify which thoughts you repeatedly think about and plan to take action. Distract yourself by watching tv, reading a book, or doing something physical. Take the mistakes you have made in the past as lessons so you won’t repeat them again. You are human and it is okay to make mistakes. "
    elif (max1 == pw_avg):
        message += "You persistant worrying seems to be the highest this week. Persistently worrying about something can take a huge toll on mental energy. Don’t worry about the things you can’t control. Don’t let your irrational fears and thoughts run amuck, keep yourself grounded to what you know is true. And lastly, talk to a friend or someone you trust to let some of that worrying go. "
    elif (max1 == nt_avg):
        message += "Our analysis shows that your negative thinking is very high this week. A lot of us have negative thoughts but not many of us take steps to combat it. The first step is to recognize when you have negative thoughts and to stop the actions leading up to those thoughts. Try to find the root of those negative thoughts so you can understand where they are coming from and try to stop them. Most importantly, don’t let your negative thoughts negatively affect your confidence! "
    elif (max1 == sc_avg):
        message += "Self criticism seems to be the problem this week. Being self critical is human nature, don’t be ashamed of it! Don’t criticize your actions. If you are unhappy about something, get proactive and try to change it. Comparing yourself to others is also another big no! You are unique! Remember to laugh at yourself, keep your confidence up, and acknowledge your strengths. "
    elif (max1 == dm_avg):
        message += "You decision making needs help this week. Anxiety and poor mental health often hurt your decision making abilities. When making decisions, keep in mind that you don’t need to make the right choice every time. Make the choice that goes more naturally to you and the one you will feel most proud of. Besides, you always have tomorrow to fix your mistakes. "

    if (max2 == c_avg):
        message += "However, on the bright side, your creativity levels are looking great! Remember to keep doing creative activities like puzzles, drawing, and writing."
    elif (max2 == s_avg):
        message += "On the other hand, it looks like you're getting great sleep!"
    elif (max2 == e_avg):
        message += "On the contrary, your energy levels are looking high this week! Keep yourself active!"

    return message


@app.route("/poststats", methods = ["POST"])
@login_required
def poststats():
    overall = request.json["overall"]
    rm = request.json["rm"]
    pw = request.json["pw"]
    nt = request.json["nt"]
    sc = request.json["sc"]
    dm = request.json["dm"]
    s = request.json["s"]
    el = request.json["el"]
    c = request.json["c"]
    new_stat = Stats(user_id=current_user.id, created_date=datetime.datetime.now().date(), overall=overall, rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s)
    db.session.add(new_stat)
    db.session.commit()
    return "added stat"


@app.route("/getProgress", methods = ["GET"])
@login_required
def getProgress():
    userid = current_user.id
    q_entries = Stats.query.filter_by(user_id=userid).all()
    num_entries = len(q_entries)
    #dict = {}
    if (num_entries > 1):
        difference = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).limit(2).all()

        id1 = difference[1].id
        id2 = difference[0].id

        user_id1 = Stats.query.filter_by(id=id1).first()
        user_id2 = Stats.query.filter_by(id=id2).first()

        overall_diff = round(user_id1.overall - user_id2.overall)
        rm_diff = round(user_id1.rm - user_id2.rm)
        pw_diff = round(user_id1.pw - user_id2.pw)
        nt_diff = round(user_id1.nt - user_id2.nt)
        sc_diff = round(user_id1.sc - user_id2.sc)
        dm_diff = round(user_id1.dm - user_id2.dm)
        c_diff = round(user_id1.c - user_id2.c)
        el_diff = round(user_id1.el - user_id2.el)
        s_diff = round(user_id1.s - user_id2.s)


        dict = {
            "overall":overall_diff,
            "rm":rm_diff,
            "pw":pw_diff,
            "nt":nt_diff,
            "sc":sc_diff,
            "dm":dm_diff,
            "c":c_diff,
            "el":el_diff,
            "s":s_diff
        }
        return dict
    else:
        return "only one entry!"


@app.route("/getWeeklyProgress", methods = ["GET"])
@login_required
def getWeeklyProgress():
    weekly_quizzes = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=current_user.id).limit(7).all()
    print(weekly_quizzes)
    weekly_quizzes.reverse()
    print(weekly_quizzes)

    dict = {}

    j = 1

    while (j<=len(weekly_quizzes)) :
        for i in weekly_quizzes:
            dict["id" + str(j)] = {
                "rm":i.rm,
                "pw":i.pw,
                "nt":i.nt,
                "sc":i.sc,
                "dm":i.dm,
                "s":i.s,
                "el":i.el,
                "c":i.c
            }
            j+=1

    if (len(weekly_quizzes)!=7):
        length = len(weekly_quizzes)
        print(length)
        start = length+1
        while (start<=7):
            dict["id" + str(start)] = {
                "rm":0,
                "pw":0,
                "nt":0,
                "sc":0,
                "dm":0,
                "s":0,
                "el":0,
                "c":0
            }
            start+=1

    return dict


@app.route("/quiz1", methods = ["GET", "POST"])
@login_required
def quiz1():
    if request.method == 'POST':
        ans1 = request.json["ans1"]
        ans2 = request.json["ans2"]
        ans3 = request.json["ans3"]
        ans4 = request.json["ans4"]
        ans5 = request.json["ans5"]
        ans6 = request.json["ans6"]
        ans7 = request.json["ans7"]
        ans8 = request.json["ans8"]
        ans9 = request.json["ans9"]
        ans10 = request.json["ans10"]

        quiz1 = {
            "I tend to dwell on my problems for a long period of time and my worrying only gets worse.":ans1,
            "I often find myself thinking about what could go wrong in the future even if those thoughts are somewhat irrational.":ans2,
            "If I do well on an assignment, I think it is because of luck or fate and not because of my own skills that contributed to the success.":ans3,
            "When you look at your friends’ social media, you feel jealous and somewhat upset that your life is not as good.":ans4,
            "I often find myself dwelling on small decisions. For example, I spend days trying to choose between two pairs of shoes and often end up asking others for their opinion.":ans5,
            "I would describe myself as having low creativity.":ans6,
            "I often have “what-if” questions and make up negative scenarios about the future.":ans7,
            "When something bad happens at work or school, I feel it is because I have failed as a leader and as a team member.":ans8,
            "When given the option to either watch a movie in bed or go out for a walk, I often choose the former.":ans9,
            "I either sleep too less or too much.":ans10
        }
        return quiz1

    else:
        quiz1 = {
            "q1":"I tend to dwell on my problems for a long period of time and my worrying only gets worse.",
            "q2":"I often find myself thinking about what could go wrong in the future even if those thoughts are somewhat irrational.",
            "q3":"If I do well on an assignment, I think it is because of luck or fate and not because of my own skills that contributed to the success.",
            "q4":"When you look at your friends’ social media, you feel jealous and somewhat upset that your life is not as good.",
            "q5":"I often find myself dwelling on small decisions. For example, I spend days trying to choose between two pairs of shoes and often end up asking others for their opinion.",
            "q6":"I would describe myself as having low creativity.",
            "q7":"I often have “what-if” questions and make up negative scenarios about the future.",
            "q8":"When something bad happens at work or school, I feel it is because I have failed as a leader and as a team member.",
            "q9":"When given the option to either watch a movie in bed or go out for a walk, I often choose the former.",
            "q99":"I either sleep too less or too much."
        }
        return quiz1

@app.route('/quiz1results', methods=['POST'])
@login_required
def quiz1results():
    ans1 = request.json["ans1"]
    ans2 = request.json["ans2"]
    ans3 = request.json["ans3"]
    ans4 = request.json["ans4"]
    ans5 = request.json["ans5"]
    ans6 = request.json["ans6"]
    ans7 = request.json["ans7"]
    ans8 = request.json["ans8"]
    ans9 = request.json["ans9"]
    ans10 = request.json["ans10"]

    el = 0
    s = 0

    rm = ans1 + ans5
    pw = ans1 + ans2 + ans7
    nt = ans3 + ans2 + ans7 + ans8
    sc = ans3 + ans4 + ans8
    dm = ans5
    c = ans6
    if (ans9 == 1):
        el += 5
    elif (ans9 == 2):
        el += 4
    elif (ans9 == 3):
        el += 3
    elif (ans9 == 4):
        el += 2
    elif (ans9 == 5):
        el += 1

    if (ans10 == 1):
        s += 5
        el += 5
    elif (ans10 == 2):
        s += 4
        el += 4
    elif (ans10 == 3):
        s += 3
        el += 3
    elif (ans10 == 4):
        s += 2
        el += 2
    elif (ans10 == 5):
        s += 1
        el += 1

    rm = rm*10
    pw = round(pw*6.67)
    nt = nt*5
    sc = round(sc*6.67)
    dm = dm*10
    c = c*20
    el = el*10
    s = s*20
    overall = round((rm+pw+nt+sc+dm)/5)

    new_stat=Stats(overall=overall, created_date = datetime.datetime.now().date(), rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()

    return "quiz stats added"



@app.route("/quiz2", methods = ["GET", "POST"])
@login_required
def quiz2():
    if request.method == 'POST':
        ans1 = request.json["ans1"]
        ans2 = request.json["ans2"]
        ans3 = request.json["ans3"]
        ans4 = request.json["ans4"]
        ans5 = request.json["ans5"]
        ans6 = request.json["ans6"]
        ans7 = request.json["ans7"]
        ans8 = request.json["ans8"]
        ans9 = request.json["ans9"]
        ans10 = request.json["ans10"]

        quiz2 = {
            "I dwell about bad things that might happen in the future.":ans1,
            "When making a major decision, I often pick the first choice to avoid having to think it through.":ans2,
            "I keep replaying my anger or sadness in my mind for a very long time.":ans3,
            "You make a suggestion at work or in school but the boss or teacher does not like it. You immediately feel you are bad at your job or schoolwork.":ans4,
            "I find it hard to motivate myself.":ans5,
            "I partake in activities that don't challenge my creativity.":ans6,
            "I have irrational and negative thoughts about the future. I imagine scenarios in which the worst often happens.":ans7,
            "When I am not chosen for an assignment of any sort, I feel it is because I am unskilled as a person overall.":ans8,
            "I look down on myself when I try something new and end up failing or embarassing myself.":ans9,
            "Embarrassing and negative thoughts often keep me up at night.":ans10
        }
        return quiz2

    else:
        quiz2 = {
            "q1":"I dwell about bad things that might happen in the future.",
            "q2":"When making a major decision, I often pick the first choice to avoid having to think it through.",
            "q3":"I keep replaying my anger or sadness in my mind for a very long time.",
            "q4":"You make a suggestion at work or in school but the boss or teacher does not like it. You immediately feel you are bad at your job or schoolwork.",
            "q5":"I find it hard to motivate myself.",
            "q6":"I partake in activities that don't challenge my creativity.",
            "q7":"I have irrational and negative thoughts about the future. I imagine scenarios in which the worst often happens.",
            "q8":"When I am not chosen for an assignment of any sort, I feel it is because I am unskilled as a person overall.",
            "q9":"I look down on myself when I try something new and end up failing or embarassing myself.",
            "q99":"Embarrassing and negative thoughts often keep me up at night."
        }
        return quiz2

@app.route('/quiz2results', methods=['POST'])
@login_required
def quiz2results():
    ans1 = request.json["ans1"]
    ans2 = request.json["ans2"]
    ans3 = request.json["ans3"]
    ans4 = request.json["ans4"]
    ans5 = request.json["ans5"]
    ans6 = request.json["ans6"]
    ans7 = request.json["ans7"]
    ans8 = request.json["ans8"]
    ans9 = request.json["ans9"]
    ans10 = request.json["ans10"]

    c = 0
    s = 0

    rm = ans1 + ans3 + ans10
    pw = ans1 + ans7
    nt = ans4 + ans7 + ans8
    sc = ans4 + ans8 + ans9
    dm = ans2
    el = ans3
    if (ans5 == 5):
        el += 1
    elif (ans5 == 4):
        el += 2
    elif (ans5 == 3):
        el += 3
    elif (ans5 == 2):
        el += 4
    elif (ans5 == 1):
        el += 5

    if (ans6 == 5):
        c += 1
    elif (ans6 == 4):
        c += 2
    elif (ans6 == 3):
        c += 3
    elif (ans6 == 2):
        c += 4
    elif (ans6 == 1):
        c += 5

    if (ans10 == 5):
        s += 1
    elif (ans10 == 4):
        s += 2
    elif (ans10 == 3):
        s += 3
    elif (ans10 == 2):
        s += 4
    elif (ans10 == 1):
        s += 5

    rm = round(rm*6.67)
    pw = pw*10
    nt = round(nt*6.67)
    sc = round(sc*6.67)
    dm = dm*10
    c = c*20
    el = el*10
    s = s*20
    overall = round((rm+pw+nt+sc+dm)/5)

    new_stat=Stats(overall=overall, created_date = datetime.datetime.now().date(), rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()

    return "quiz stats added"



@app.route("/quiz3", methods = ["GET", "POST"])
@login_required
def quiz3():
    if request.method == 'POST':
        ans1 = request.json["ans1"]
        ans2 = request.json["ans2"]
        ans3 = request.json["ans3"]
        ans4 = request.json["ans4"]
        ans5 = request.json["ans5"]
        ans6 = request.json["ans6"]
        ans7 = request.json["ans7"]
        ans8 = request.json["ans8"]
        ans9 = request.json["ans9"]
        ans10 = request.json["ans10"]

        quiz3 = {
            "I feel terrible about myself when my eating gets out of control.":ans1,
            "When someone of higher authority wants to speak to me, I automatically assume they want to discuss something negative.":ans2,
            "When I feel sad or angry, I keep thinking about how bad I feel.":ans3,
            "When trying to sleep, I often feel overwhelmed by negative thoughts.":ans4,
            "When making any kind of choice, I find myself thinking of everything that can go wrong and that causes me to follow others’ opinions and suggestions.":ans5,
            "I often dwell on one thought or a string of the same thoughts for hours at a time.":ans6,
            "Most of the time, I feel drained and unmotivated to do anything.":ans7,
            "I don't like to participate in activities that require creativity.":ans8,
            "When something does not go right, you feel you are the one to blame and cannot fix things.":ans9,
            "Everything must go right or I feel I am incompetent.":ans10
        }
        return quiz3

    else:
        quiz3 = {
            "q1":"I feel terrible about myself when my eating gets out of control.",
            "q2":"When someone of higher authority wants to speak to me, I automatically assume they want to discuss something negative.",
            "q3":"When I feel sad or angry, I keep thinking about how bad I feel.",
            "q4":"When trying to sleep, I often feel overwhelmed by negative thoughts.",
            "q5":"When making any kind of choice, I find myself thinking of everything that can go wrong and that causes me to follow others’ opinions and suggestions.",
            "q6":"I often dwell on one thought or a string of the same thoughts for hours at a time.",
            "q7":"Most of the time, I feel drained and unmotivated to do anything.",
            "q8":"I don't like to participate in activities that require creativity.",
            "q9":"When something does not go right, you feel you are the one to blame and cannot fix things.",
            "q99":"Everything must go right or I feel I am incompetent."
        }
        return quiz3


@app.route('/quiz3results', methods=['POST'])
@login_required
def quiz3results():
    ans1 = request.json["ans1"]
    ans2 = request.json["ans2"]
    ans3 = request.json["ans3"]
    ans4 = request.json["ans4"]
    ans5 = request.json["ans5"]
    ans6 = request.json["ans6"]
    ans7 = request.json["ans7"]
    ans8 = request.json["ans8"]
    ans9 = request.json["ans9"]
    ans10 = request.json["ans10"]

    el = 0
    s = 0
    c = 0

    rm = ans3 + ans6
    pw = ans5 + ans6
    nt = ans2 + ans4 + ans9
    sc = ans1 + ans2 + ans9 + ans10
    dm = ans5

    if (ans4 == 5):
        s += 1
    elif (ans4 == 4):
        s += 2
    elif (ans4 == 3):
        s += 3
    elif (ans4 == 2):
        s += 4
    elif (ans4 == 1):
        s += 5

    if (ans7 == 5):
        s += 1
        el += 1
    elif (ans7 == 4):
        s += 2
        el += 2
    elif (ans7 == 3):
        s += 3
        el += 3
    elif (ans7 == 2):
        s += 4
        el += 4
    elif (ans7 == 1):
        s += 5
        el += 5

    if (ans8 == 5):
        c += 1
    elif (ans8 == 4):
        c += 2
    elif (ans8 == 3):
        c += 3
    elif (ans8 == 2):
        c += 4
    elif (ans8 == 1):
        c += 5

    rm = rm*10
    pw = pw*10
    nt = round(nt*6.67)
    sc = sc * 5
    dm = dm*10
    c = c*20
    el = el*20
    s = s*10
    overall = round((rm+pw+nt+sc+dm)/5)

    new_stat=Stats(overall=overall, created_date = datetime.datetime.now().date(), rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()

    return "quiz stats added"


@app.route("/quiz4", methods = ["GET", "POST"])
@login_required
def quiz4():
    if request.method == 'POST':
        ans1 = request.json["ans1"]
        ans2 = request.json["ans2"]
        ans3 = request.json["ans3"]
        ans4 = request.json["ans4"]
        ans5 = request.json["ans5"]
        ans6 = request.json["ans6"]
        ans7 = request.json["ans7"]
        ans8 = request.json["ans8"]
        ans9 = request.json["ans9"]
        ans10 = request.json["ans10"]

        quiz4 = {
            "When trying to sleep, I find myself having the same negative thoughts in a kind of loop that never ends.":ans1,
            "I go over embarrassing or awkward moments in my mind again and again.":ans2,
            "I find it hard to sleep and find it hard to wake up.":ans3,
            "When someone comes to you for advice on a decision, you often fail to give a decisive and clear answer stating your opinion.":ans4,
            "It is unacceptable for me to make mistakes even when I am learning something new.":ans5,
            "I always worry about and judge things in the present by my past experiences.":ans6,
            "I would say I am usually drained of energy.":ans7,
            "I dislike and am not very good at drawing pictures and imagining things.":ans8,
            "Minor things and mistakes usually become a big deal for me and I worry about them excessively.":ans9,
            "It usually takes a long time for me to forgive myself.":ans10
        }
        return quiz4

    else:
        quiz4 = {
            "q1":"When trying to sleep, I find myself having the same negative thoughts in a kind of loop that never ends.",
            "q2":"I go over embarrassing or awkward moments in my mind again and again.",
            "q3":"I find it hard to sleep and find it hard to wake up.",
            "q4":"When someone comes to you for advice on a decision, you often fail to give a decisive and clear answer stating your opinion.",
            "q5":"It is unacceptable for me to make mistakes even when I am learning something new.",
            "q6":"I always worry and judge things in the present by my past experiences.",
            "q7":"I would say I am usually drained of energy.",
            "q8":"I dislike and am not very good at drawing pictures and imagining things.",
            "q9":"Minor things and mistakes usually become a big deal for me and I worry about them excessively.",
            "q99":"It usually takes a long time for me to forgive myself."
        }
        return quiz4


@app.route('/quiz4results', methods=['POST'])
@login_required
def quiz4results():
    ans1 = request.json["ans1"]
    ans2 = request.json["ans2"]
    ans3 = request.json["ans3"]
    ans4 = request.json["ans4"]
    ans5 = request.json["ans5"]
    ans6 = request.json["ans6"]
    ans7 = request.json["ans7"]
    ans8 = request.json["ans8"]
    ans9 = request.json["ans9"]
    ans10 = request.json["ans10"]

    el = 0
    s = 0
    c = 0

    rm = ans2 + ans6
    pw = ans1 + ans9
    nt = ans2 + ans6
    sc = ans5 + ans10
    dm = ans4

    if (ans3 == 5):
        s += 1
    elif (ans3 == 4):
        s += 2
    elif (ans3 == 3):
        s += 3
    elif (ans3 == 2):
        s += 4
    elif (ans3 == 1):
        s += 5

    if (ans7 == 5):
        el += 1
    elif (ans7 == 4):
        el += 2
    elif (ans7 == 3):
        el += 3
    elif (ans7 == 2):
        el += 4
    elif (ans7 == 1):
        el += 5

    if (ans8 == 5):
        c += 1
    elif (ans8 == 4):
        c += 2
    elif (ans8 == 3):
        c += 3
    elif (ans8 == 2):
        c += 4
    elif (ans8 == 1):
        c += 5

    rm = rm*10
    pw = pw*10
    nt = nt*10
    sc = sc*10
    dm = dm*10
    c = c*20
    el = el*20
    s = s*10
    overall = round((rm+pw+nt+sc+dm)/5)

    new_stat=Stats(overall=overall, created_date = datetime.datetime.now().date(), rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()

    return "quiz stats added"



@app.route("/quiz5", methods = ["GET", "POST"])
@login_required
def quiz5():
    if request.method == 'POST':
        ans1 = request.json["ans1"]
        ans2 = request.json["ans2"]
        ans3 = request.json["ans3"]
        ans4 = request.json["ans4"]
        ans5 = request.json["ans5"]
        ans6 = request.json["ans6"]
        ans7 = request.json["ans7"]
        ans8 = request.json["ans8"]
        ans9 = request.json["ans9"]
        ans10 = request.json["ans10"]

        quiz5 = {
            "If someone disagrees with me, I believe he/she doesn’t like me.":ans1,
            "After accomplishing a goal I have worked towards for a long time, I don't give myself the credit and respect I deserve.":ans2,
            "When making decisions, I must always choose the right one or everything will not turn out how I want it.":ans3,
            "My sleep is broken due to thoughts keeping me up at night.":ans4,
            "My friends and family would not describe me as a creative person.":ans5,
            "My past mistakes, embarrassments, and bad decisions run in my mind for hours at a time.":ans6,
            "While working on an assignment or project, I worry about all the things that might go wrong. This can sometimes even stop me from trying my hardest.":ans7,
            "I would say that most of my day is filled with inactive and unenergetic tasks.":ans8,
            "I find myself constantly worrying and I can feel it draining my energy.":ans9,
            "I have a tendency to blame myself for anything that goes wrong.":ans10
        }
        return quiz5

    else:
        quiz5 = {
            "q1":"If someone disagrees with you, you believe he/she doesn’t like you.",
            "q2":"After accomplishing a goal I have worked towards for a long time, I don't give myself the credit and respect I deserve.",
            "q3":"When making decisions, I must always choose the right one or everything will not turn out how I want it.",
            "q4":"My sleep is broken due to thoughts keeping me up at night.",
            "q5":"My friends and family would not describe me as a creative person.",
            "q6":"My past mistakes, embarrassments, and bad decisions run in my mind for hours at a time.",
            "q7":"While working on an assignment or project, I worry about all the things that might go wrong. This can sometimes even stop me from trying my hardest.",
            "q8":"I would say that most of my day is filled with inactive and unenergetic tasks.",
            "q9":"I find myself constantly worrying and I can feel it draining my energy.",
            "q99":"I have a tendency to blame myself for anything that goes wrong."
        }
        return quiz5

@app.route('/quiz5results', methods=['POST'])
@login_required
def quiz5results():
    ans1 = request.json["ans1"]
    ans2 = request.json["ans2"]
    ans3 = request.json["ans3"]
    ans4 = request.json["ans4"]
    ans5 = request.json["ans5"]
    ans6 = request.json["ans6"]
    ans7 = request.json["ans7"]
    ans8 = request.json["ans8"]
    ans9 = request.json["ans9"]
    ans10 = request.json["ans10"]

    s = 0
    el = 0
    c = 0

    rm = ans4 + ans6
    pw = ans7 + ans9
    nt = ans2 + ans3
    sc = ans1 + ans2 + ans10
    dm = ans3

    if (ans4 == 5):
        s += 1
    elif (ans4 == 4):
        s += 2
    elif (ans4 == 3):
        s += 3
    elif (ans4 == 2):
        s += 4
    elif (ans4 == 1):
        s += 5

    if (ans5 == 5):
        c += 1
    elif (ans5 == 4):
        c += 2
    elif (ans5 == 3):
        c += 3
    elif (ans5 == 2):
        c += 4
    elif (ans5 == 1):
        c += 5

    if (ans8 == 5):
        el += 1
    elif (ans8 == 4):
        el += 2
    elif (ans8 == 3):
        el += 3
    elif (ans8 == 2):
        el += 4
    elif (ans8 == 1):
        el += 5

    if (ans9 == 5):
        el += 1
    elif (ans9 == 4):
        el += 2
    elif (ans9 == 3):
        el += 3
    elif (ans9 == 2):
        el += 4
    elif (ans9 == 1):
        el += 5

    rm = rm*10
    pw = pw*10
    nt = nt*10
    sc = round(sc*6.67)
    dm = dm*10
    c = c*20
    el = el*10
    s = s*20
    overall = round((rm+pw+nt+sc+dm)/5)

    new_stat=Stats(overall=overall, created_date = datetime.datetime.now().date(), rm=rm, pw=pw, nt=nt, sc=sc, dm=dm, c=c, el=el, s=s, user_id=current_user.id)
    db.session.add(new_stat)
    db.session.commit()

    return "quiz stats added"


@app.route('/takeQuiz', methods = ["GET"])
@login_required
def takeQuiz():
    userid = current_user.id
    user = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).first()

    if user is not None:
        new_day = datetime.timedelta(days=1)
        latest_date = user.created_date
        print(latest_date)
        last_day = datetime.datetime.strptime(latest_date, '%Y-%m-%d')
        target = new_day + last_day
        today = datetime.datetime.now().date()
        target_date = target.date()
    #str_today = str(today)
    #str_target = str(target_date)
        print(latest_date)
        print(today)
        print()
        print(target_date)
        print(today)
        if target_date <= today:
            return "true"
        else:
            return "false"
    else:
        return "true"

@app.route('/whatactivity', methods = ["GET"])
@login_required
def whatactivity():
    userid = current_user.id
    act = ""
    last_quiz = Stats.query.order_by(Stats.id.desc()).filter_by(user_id=userid).first()
    maxnum = max(last_quiz.rm, last_quiz.pw, last_quiz.nt, last_quiz.sc, last_quiz.dm)
    if (last_quiz.rm == maxnum):
        act = "rm"
    elif (last_quiz.pw == maxnum):
        act = "pw"
    elif (last_quiz.nt == maxnum):
        act = "nt"
    elif (last_quiz.sc == maxnum):
        act = "sc"
    elif (last_quiz.dm == maxnum):
        act = "dm"

    return act

def findact(database, user, date):
    act = database.query.filter_by(user_id=user).all()
    for i in act:
        d = str(i.created_date.date())
        t = str(date)
        if (d==t):
            return act
    #print(act.thought)
    return None

@app.route('/activityView', methods=["GET"])
def activityView():
    today = datetime.datetime.now().date()
    num = 0
    rm1 = findact(rmchange, current_user.id, today)
    rm2 = findact(rmpast, current_user.id, today)
    pw1 = findact(pwcontrol, current_user.id, today)
    pw2 = findact(pwevidence, current_user.id, today)
    sc1 = findact(scchange, current_user.id, today)
    sc2 = findact(scgood, current_user.id, today)
    nt1 = findact(ntpositive, current_user.id, today)
    nt2 = findact(nttrue, current_user.id, today)
    dm1 = findact(dmnow, current_user.id, today)
    dm2 = findact(dmworst, current_user.id, today)

    if rm1 is not None:
        print("rmchange")
        num+=1
    if rm2 is not None:
        print("rmpast")
        num+=1
    if pw1 is not None:
        print("pwcontrol")
        num+=1
    if pw2 is not None:
        print("pwevidence")
        num+=1
    if sc1 is not None:
        print("scchange")
        num+=1
    if sc2 is not None:
        print("scgood")
        num+=1
    if nt1 is not None:
        print("ntpositive")
        num+=1
    if nt2 is not None:
        print("nttrue")
        num+=1
    if dm1 is not None:
        print("dmnow")
        num+=1
    if dm2 is not None:
        print("dmworst")
        num+=1

    if (num==0):
        return "no activity"
    else:
        return "activity"


@app.route('/alltests', methods = ["GET"])
@login_required
def alltests():
    all_tests = Stats.query.filter_by(user_id=current_user.id).all()
    print(all_tests)
    test_dates = []
    dict = {}
    for i in all_tests:
        num = 0
        date = i.created_date
        #print(date)
        rm1 = findact(rmchange, current_user.id, date)
        rm2 = findact(rmpast, current_user.id, date)
        pw1 = findact(pwcontrol, current_user.id, date)
        pw2 = findact(pwevidence, current_user.id, date)
        sc1 = findact(scchange, current_user.id, date)
        sc2 = findact(scgood, current_user.id, date)
        nt1 = findact(ntpositive, current_user.id, date)
        nt2 = findact(nttrue, current_user.id, date)
        dm1 = findact(dmnow, current_user.id, date)
        dm2 = findact(dmworst, current_user.id, date)
        if rm1 is not None:
            print("rmchange")
            num+=1
        if rm2 is not None:
            print("rmpast")
            num+=1
        if pw1 is not None:
            print("pwcontrol")
            num+=1
        if pw2 is not None:
            print("pwevidence")
            num+=1
        if sc1 is not None:
            print("scchange")
            num+=1
        if sc2 is not None:
            print("scgood")
            num+=1
        if nt1 is not None:
            print("ntpositive")
            num+=1
        if nt2 is not None:
            print("nttrue")
            num+=1
        if dm1 is not None:
            print("dmnow")
            num+=1
        if dm2 is not None:
            print("dmworst")
            num+=1

        print(num)

        if (num != 0):
            test_dates.append(date)

    #print(test_dates[0])

    dict["dates"] = test_dates


    return dict


def my_list(database):
    l_thoughts = database.query.filter_by(user_id=current_user.id, suggestion=" ").all()
    list_thoughts = []
    for i in l_thoughts:
        date1 = str(i.created_date.date())
        date2 = str(date.today())
        if date1 == date2:
            list_thoughts.append(i)
    return list_thoughts

def my_list_control(database):
    userid = current_user.id
    l_thoughts = database.query.order_by(database.id.desc()).filter_by(user_id=userid, control=True, suggestion=" ").limit(5).all()
    #list_thoughts = []
    print(l_thoughts)
    '''
    for i in l_thoughts:
        date1 = str(i.created_date.date())
        print("date 1 is:")
        print(date1)
        date2 = str(datetime.datetime.now().date())
        print("date2 is: ")
        print(date2)
        if date1 == date2:
            list_thoughts.append(i)
            '''

    return l_thoughts


@app.route('/whatwentwrong', methods=["POST","GET"])
@login_required
def whatwentwrong():
    input1 = request.json["input1"]
    new = rmchange(user_id=current_user.id, thought=input1, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = rmchange(user_id=current_user.id, thought=input2, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = rmchange(user_id=current_user.id, thought=input3, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = rmchange(user_id=current_user.id, thought=input4, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = rmchange(user_id=current_user.id, thought=input5, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getrmchange', methods= ["GET"])
@login_required
def getrmchange():
    l = my_list(rmchange)
    dict = {}
    print(len(l))
    dict = {
        "thought1":l[0].thought,
        "thought2":l[1].thought,
        "thought3":l[2].thought,
        "thought4":l[3].thought,
        "thought5":l[4].thought
     }

    return dict

@app.route('/whatwouldichange', methods=["POST","GET"])
@login_required
def whatwouldichange():
    if request.method == "POST":
        l = my_list(rmchange)
        length = len(l)

        sug1 = request.json["sug1"]
        sug2 = request.json["sug2"]
        sug3 = request.json["sug3"]
        sug4 = request.json["sug4"]
        sug5 = request.json["sug5"]

        array = [sug1, sug2, sug3, sug4, sug5]
        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"



@app.route('/rightinthepast', methods=["POST","GET"])
@login_required
def rightinthepast():
    input1 = request.json["input1"]
    new = rmpast(user_id=current_user.id, thought=input1)
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = rmpast(user_id=current_user.id, thought=input2)
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = rmpast(user_id=current_user.id, thought=input3)
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = rmpast(user_id=current_user.id, thought=input4)
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = rmpast(user_id=current_user.id, thought=input5)
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity


@app.route('/negativethoughts', methods=["POST","GET"])
@login_required
def negativethoughts():
    input1 = request.json["input1"]
    new = ntpositive(user_id=current_user.id, thought=input1, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = ntpositive(user_id=current_user.id, thought=input2, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = ntpositive(user_id=current_user.id, thought=input3, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = ntpositive(user_id=current_user.id, thought=input4, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = ntpositive(user_id=current_user.id, thought=input5, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getntpositive', methods= ["GET"])
@login_required
def getntpositive():
    l = my_list(ntpositive)
    dict = {}
    print(len(l))
    dict = {
        "thought1":l[0].thought,
        "thought2":l[1].thought,
        "thought3":l[2].thought,
        "thought4":l[3].thought,
        "thought5":l[4].thought
     }

    return dict

@app.route('/positivespin', methods=["POST","GET"])
@login_required
def positivespin():
    if request.method == "POST":
        l = my_list(ntpositive)
        length = len(l)

        sug1 = request.json["sug1"]
        sug2 = request.json["sug2"]
        sug3 = request.json["sug3"]
        sug4 = request.json["sug4"]
        sug5 = request.json["sug5"]

        array = [sug1, sug2, sug3, sug4, sug5]
        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"


@app.route('/goodqualities', methods=["POST","GET"])
@login_required
def goodqualities():
    input1 = request.json["input1"]
    new = scgood(user_id=current_user.id, thought=input1)
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = scgood(user_id=current_user.id, thought=input2)
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = scgood(user_id=current_user.id, thought=input3)
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = scgood(user_id=current_user.id, thought=input4)
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = scgood(user_id=current_user.id, thought=input5)
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity


@app.route('/selfcriticism', methods=["POST","GET"])
@login_required
def selfcriticism():
    input1 = request.json["input1"]
    new = screword(user_id=current_user.id, thought=input1, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = screword(user_id=current_user.id, thought=input2, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = screword(user_id=current_user.id, thought=input3, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = screword(user_id=current_user.id, thought=input4, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = screword(user_id=current_user.id, thought=input5, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getscreword', methods= ["GET"])
@login_required
def getscreword():
    l = my_list(screword)
    dict = {}
    print(len(l))
    dict = {
        "thought1":l[0].thought,
        "thought2":l[1].thought,
        "thought3":l[2].thought,
        "thought4":l[3].thought,
        "thought5":l[4].thought
     }

    return dict

@app.route('/reword', methods=["POST","GET"])
@login_required
def reword():
    if request.method == "POST":
        l = my_list(screword)
        length = len(l)

        sug1 = request.json["sug1"]
        sug2 = request.json["sug2"]
        sug3 = request.json["sug3"]
        sug4 = request.json["sug4"]
        sug5 = request.json["sug5"]

        array = [sug1, sug2, sug3, sug4, sug5]
        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"


@app.route('/decisions', methods=["POST","GET"])
@login_required
def decisions():
    input1 = request.json["input1"]
    new = dmworst(user_id=current_user.id, thought=input1, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = dmworst(user_id=current_user.id, thought=input2, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = dmworst(user_id=current_user.id, thought=input3, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = dmworst(user_id=current_user.id, thought=input4, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = dmworst(user_id=current_user.id, thought=input5, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getdmworst', methods= ["GET"])
@login_required
def getdmworst():
    l = my_list(dmworst)
    dict = {}
    print(len(l))
    dict = {
        "thought1":l[0].thought,
        "thought2":l[1].thought,
        "thought3":l[2].thought,
        "thought4":l[3].thought,
        "thought5":l[4].thought
     }

    return dict

@app.route('/worstthatcanhappen', methods=["POST","GET"])
@login_required
def worstthatcanhappen():
    if request.method == "POST":
        l = my_list(dmworst)
        length = len(l)

        sug1 = request.json["sug1"]
        sug2 = request.json["sug2"]
        sug3 = request.json["sug3"]
        sug4 = request.json["sug4"]
        sug5 = request.json["sug5"]

        array = [sug1, sug2, sug3, sug4, sug5]
        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"



@app.route('/canihelpnow', methods=["POST","GET"])
@login_required
def canihelpnow():
    input1 = request.json["input1"]
    new = dmnow(user_id=current_user.id, thought=input1, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    new = dmnow(user_id=current_user.id, thought=input2, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    new = dmnow(user_id=current_user.id, thought=input3, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    new = dmnow(user_id=current_user.id, thought=input4, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    new = dmnow(user_id=current_user.id, thought=input5, suggestion=" ")
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "input2":input2,
        "input3":input3,
        "input4":input4,
        "input5":input5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getdmnow', methods= ["GET"])
@login_required
def getdmnow():
    l = my_list(dmnow)
    dict = {}
    print(len(l))
    dict = {
        "thought1":l[0].thought,
        "thought2":l[1].thought,
        "thought3":l[2].thought,
        "thought4":l[3].thought,
        "thought5":l[4].thought
     }

    return dict

@app.route('/howcanihelp', methods=["POST","GET"])
@login_required
def howcanihelp():
    if request.method == "POST":
        l = my_list(dmnow)
        length = len(l)

        sug1 = request.json["sug1"]
        sug2 = request.json["sug2"]
        sug3 = request.json["sug3"]
        sug4 = request.json["sug4"]
        sug5 = request.json["sug5"]

        array = [sug1, sug2, sug3, sug4, sug5]
        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"

@app.route('/doihavecontrol', methods=["POST","GET"])
@login_required
def doihavecontrol():
    input1 = request.json["input1"]
    control1 = request.json["control1"]
    new = pwcontrol(user_id=current_user.id, thought=input1, suggestion=" ", control=control1)
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    control2 = request.json["control2"]
    new = pwcontrol(user_id=current_user.id, thought=input2, suggestion=" ", control=control2)
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    control3 = request.json["control3"]
    new = pwcontrol(user_id=current_user.id, thought=input3, suggestion=" ", control=control3)
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    control4 = request.json["control4"]
    new = pwcontrol(user_id=current_user.id, thought=input4, suggestion=" ", control=control4)
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    control5 = request.json["control5"]
    new = pwcontrol(user_id=current_user.id, thought=input5, suggestion=" ", control=control5)
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "control1":control1,
        "input2":input2,
        "control2":control2,
        "input3":input3,
        "control3":control3,
        "input4":input4,
        "control4":control4,
        "input5":input5,
        "control5":control5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getpwcontrol', methods= ["GET"])
@login_required
def getpwcontrol():
    l = my_list_control(pwcontrol)
    dict = {}
    print(len(l))
    if len(l) == 5:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":l[4].thought
        }
    elif len(l) == 4:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":""
        }
    elif len(l) == 3:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 2:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 1:
        dict = {
            "thought1":l[0].thought,
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    else:
        dict = {
            "thought1":"",
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }

    return dict


@app.route('/whatcanido', methods=["POST","GET"])
@login_required
def whatcanido():
    if request.method == "POST":
        l = my_list_control(pwcontrol)
        length = len(l)
        array = []

        if (length == 5):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]
            sug5 = request.json["sug5"]

            array = [sug1, sug2, sug3, sug4, sug5]
        elif (length == 4):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]

            array = [sug1, sug2, sug3, sug4]
        elif (length == 3):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]

            array = [sug1, sug2, sug3]
        elif (length == 2):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]

            array = [sug1, sug2]
        elif (length == 1):
            sug1 = request.json["sug1"]

            array = [sug1]

        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"


@app.route('/howlikelytohappen', methods=["POST","GET"])
@login_required
def howlikelytohappen():
    input1 = request.json["input1"]
    control1 = request.json["control1"]
    new = pwevidence(user_id=current_user.id, thought=input1, suggestion=" ", control=control1)
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    control2 = request.json["control2"]
    new = pwevidence(user_id=current_user.id, thought=input2, suggestion=" ", control=control2)
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    control3 = request.json["control3"]
    new = pwevidence(user_id=current_user.id, thought=input3, suggestion=" ", control=control3)
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    control4 = request.json["control4"]
    new = pwevidence(user_id=current_user.id, thought=input4, suggestion=" ", control=control4)
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    control5 = request.json["control5"]
    new = pwevidence(user_id=current_user.id, thought=input5, suggestion=" ", control=control5)
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "control1":control1,
        "input2":input2,
        "control2":control2,
        "input3":input3,
        "control3":control3,
        "input4":input4,
        "control4":control4,
        "input5":input5,
        "control5":control5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getpwevidence', methods= ["GET"])
@login_required
def getpwevidence():
    l = my_list_control(pwevidence)
    dict = {}
    print(len(l))
    if len(l) == 5:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":l[4].thought
        }
    elif len(l) == 4:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":""
        }
    elif len(l) == 3:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 2:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 1:
        dict = {
            "thought1":l[0].thought,
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    else:
        dict = {
            "thought1":"",
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }

    return dict


@app.route('/evidence', methods=["POST","GET"])
@login_required
def evidence():
    if request.method == "POST":
        l = my_list_control(pwevidence)
        length = len(l)
        array = []

        if (length == 5):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]
            sug5 = request.json["sug5"]

            array = [sug1, sug2, sug3, sug4, sug5]
        elif (length == 4):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]

            array = [sug1, sug2, sug3, sug4]
        elif (length == 3):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]

            array = [sug1, sug2, sug3]
        elif (length == 2):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]

            array = [sug1, sug2]
        elif (length == 1):
            sug1 = request.json["sug1"]

            array = [sug1]

        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"


@app.route('/isittrue', methods=["POST","GET"])
@login_required
def isittrue():
    input1 = request.json["input1"]
    control1 = request.json["control1"]
    new = nttrue(user_id=current_user.id, thought=input1, suggestion=" ", control=control1)
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    control2 = request.json["control2"]
    new = nttrue(user_id=current_user.id, thought=input2, suggestion=" ", control=control2)
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    control3 = request.json["control3"]
    new = nttrue(user_id=current_user.id, thought=input3, suggestion=" ", control=control3)
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    control4 = request.json["control4"]
    new = nttrue(user_id=current_user.id, thought=input4, suggestion=" ", control=control4)
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    control5 = request.json["control5"]
    new = nttrue(user_id=current_user.id, thought=input5, suggestion=" ", control=control5)
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "control1":control1,
        "input2":input2,
        "control2":control2,
        "input3":input3,
        "control3":control3,
        "input4":input4,
        "control4":control4,
        "input5":input5,
        "control5":control5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getnttrue', methods= ["GET"])
@login_required
def getnttrue():
    l = my_list_control(nttrue)
    dict = {}
    print(len(l))
    if len(l) == 5:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":l[4].thought
        }
    elif len(l) == 4:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":""
        }
    elif len(l) == 3:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 2:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 1:
        dict = {
            "thought1":l[0].thought,
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    else:
        dict = {
            "thought1":"",
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }

    return dict


@app.route('/whyisittrue', methods=["POST","GET"])
@login_required
def whyisittrue():
    if request.method == "POST":
        l = my_list_control(nttrue)
        length = len(l)
        array = []

        if (length == 5):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]
            sug5 = request.json["sug5"]

            array = [sug1, sug2, sug3, sug4, sug5]
        elif (length == 4):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]

            array = [sug1, sug2, sug3, sug4]
        elif (length == 3):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]

            array = [sug1, sug2, sug3]
        elif (length == 2):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]

            array = [sug1, sug2]
        elif (length == 1):
            sug1 = request.json["sug1"]

            array = [sug1]

        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"


@app.route('/canichangeit', methods=["POST","GET"])
@login_required
def canichangeit():
    input1 = request.json["input1"]
    control1 = request.json["control1"]
    new = scchange(user_id=current_user.id, thought=input1, suggestion=" ", control=control1)
    db.session.add(new)
    db.session.commit()
    input2 = request.json["input2"]
    control2 = request.json["control2"]
    new = scchange(user_id=current_user.id, thought=input2, suggestion=" ", control=control2)
    db.session.add(new)
    db.session.commit()
    input3 = request.json["input3"]
    control3 = request.json["control3"]
    new = scchange(user_id=current_user.id, thought=input3, suggestion=" ", control=control3)
    db.session.add(new)
    db.session.commit()
    input4 = request.json["input4"]
    control4 = request.json["control4"]
    new = scchange(user_id=current_user.id, thought=input4, suggestion=" ", control=control4)
    db.session.add(new)
    db.session.commit()
    input5 = request.json["input5"]
    control5 = request.json["control5"]
    new = scchange(user_id=current_user.id, thought=input5, suggestion=" ", control=control5)
    db.session.add(new)
    db.session.commit()
    activity = {
        "input1":input1,
        "control1":control1,
        "input2":input2,
        "control2":control2,
        "input3":input3,
        "control3":control3,
        "input4":input4,
        "control4":control4,
        "input5":input5,
        "control5":control5
    }
    if request.method == "POST":
        return "added thoughts"
    else:
        return activity

@app.route('/getscchange', methods= ["GET"])
@login_required
def getscchange():
    l = my_list_control(scchange)
    dict = {}
    print(len(l))
    if len(l) == 5:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":l[4].thought
        }
    elif len(l) == 4:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":l[3].thought,
            "thought5":""
        }
    elif len(l) == 3:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":l[2].thought,
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 2:
        dict = {
            "thought1":l[0].thought,
            "thought2":l[1].thought,
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    elif len(l) == 1:
        dict = {
            "thought1":l[0].thought,
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }
    else:
        dict = {
            "thought1":"",
            "thought2":"",
            "thought3":"",
            "thought4":"",
            "thought5":""
        }

    return dict


@app.route('/howcanichangeit', methods=["POST","GET"])
@login_required
def howcanichangeit():
    if request.method == "POST":
        l = my_list_control(scchange)
        length = len(l)
        array = []

        if (length == 5):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]
            sug5 = request.json["sug5"]

            array = [sug1, sug2, sug3, sug4, sug5]
        elif (length == 4):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]
            sug4 = request.json["sug4"]

            array = [sug1, sug2, sug3, sug4]
        elif (length == 3):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]
            sug3 = request.json["sug3"]

            array = [sug1, sug2, sug3]
        elif (length == 2):
            sug1 = request.json["sug1"]
            sug2 = request.json["sug2"]

            array = [sug1, sug2]
        elif (length == 1):
            sug1 = request.json["sug1"]

            array = [sug1]

        i = 0
        while(i<length):
            l[i].suggestion = array[i]
            db.session.commit()
            i+=1

        return "success"


def getrecords(database, date, userid):
    last_activity = []
    activity = database.query.filter_by(user_id=userid).all()
    #print("the list of activites are: ")
    #print(activity)
    for i in activity:
        date1 = str(i.created_date.date())
        if (date == date1):
            last_activity.append(i)

    print("the activities are: ")
    print(last_activity)
    return last_activity

@app.route('/getdaterecords', methods = ["GET","POST"])
@login_required
def getdaterecords():
    if request.method == "POST":
        date_activity = []
        dict = {}
        db = 0
        act = ""
        thought = []
        suggestion = []
        control = []
        date = request.json["date"]
        user = current_user.id
        print(date)
        a_rmpast = getrecords(rmpast,date,user)
        print("inside route")
        print(a_rmpast)
        if (len(a_rmpast)!=0):
            date_activity = a_rmpast
            db = 1
            act = "Right in the Past"

        a_rmchange = getrecords(rmchange,date,user)
        print("inside route")
        print(a_rmchange)
        if (len(a_rmchange)!=0):
            date_activity = a_rmchange
            db = 2
            act = "What Went Wrong"

        a_pwcontrol = getrecords(pwcontrol,date,user)
        print("inside route")
        print(a_pwcontrol)
        if (len(a_pwcontrol)!=0):
            date_activity = a_pwcontrol
            db = 3
            act = "Do I Have Control?"

        a_pwevidence = getrecords(pwevidence,date,user)
        print("inside route")
        print(a_pwevidence)
        if (len(a_pwevidence)!=0):
            date_activity = a_pwevidence
            db = 3
            act = "Will it Happen?"

        a_scchange = getrecords(scchange,date,user)
        print("inside route")
        print(a_scchange)
        if (len(a_scchange)!=0):
            date_activity = a_scchange
            db = 3
            act = "Can I Change it?"

        a_scgood = getrecords(scgood,date,user)
        print("inside route")
        print(a_scgood)
        if (len(a_scgood)!=0):
            date_activity = a_scgood
            db = 1
            act = "What I Love About Me"

        a_nttrue = getrecords(nttrue,date,user)
        print("inside route")
        print(a_nttrue)
        if (len(a_nttrue)!=0):
            date_activity = a_nttrue
            db = 3
            act = "It is True?"

        a_ntpositive = getrecords(ntpositive,date,user)
        print("inside route")
        print(a_ntpositive)
        if (len(a_ntpositive)!=0):
            date_activity = a_ntpositive
            db = 2
            act = "Positive Spin"

        a_dmnow = getrecords(dmnow,date,user)
        print("inside route")
        print(a_dmnow)
        if (len(a_dmnow)!=0):
            date_activity = a_dmnow
            db = 2
            act = "Can I Help Now?"

        a_dmworst = getrecords(dmworst,date,user)
        print("inside route")
        print(a_dmworst)
        if (len(a_dmworst)!=0):
            date_activity = a_dmworst
            db = 2
            act = "Worst That Can Happen"

        print(date_activity)
        if (db == 1):
            for i in date_activity:
                thought.append(i.thought)

            dict = {
                "db":db,
                "act":act,
                "thought1":thought[0],
                "thought2":thought[1],
                "thought3":thought[2],
                "thought4":thought[3],
                "thought5":thought[4]
            }
        elif (db == 2):
            for i in date_activity:
                thought.append(i.thought)
                suggestion.append(i.suggestion)

            dict = {
                "db":db,
                "act":act,
                "thought1":thought[0],
                "thought2":thought[1],
                "thought3":thought[2],
                "thought4":thought[3],
                "thought5":thought[4],
                "suggestion1":suggestion[0],
                "suggestion2":suggestion[1],
                "suggestion3":suggestion[2],
                "suggestion4":suggestion[3],
                "suggestion5":suggestion[4]
            }
        elif (db == 3):
            for i in date_activity:
                thought.append(i.thought)
                suggestion.append(i.suggestion)
                control.append(i.control)

            dict = {
                "db":db,
                "act":act,
                "thought1":thought[0],
                "thought2":thought[1],
                "thought3":thought[2],
                "thought4":thought[3],
                "thought5":thought[4],
                "suggestion1":suggestion[0],
                "suggestion2":suggestion[1],
                "suggestion3":suggestion[2],
                "suggestion4":suggestion[3],
                "suggestion5":suggestion[4],
                "control1":control[0],
                "control2":control[1],
                "control3":control[2],
                "control4":control[3],
                "control5":control[4]
            }

        return dict





if __name__ == '__main__':
    app.run(debug=True)









#
