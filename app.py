# Implements a registration form, confirming registration via email

import os
import re
from cs50 import SQL
from flask import Flask, render_template, request, session
from flask_mail import Mail, Message
from string import Template
from flask_session import Session
from login import login_required

app = Flask(__name__)
# template for email code from https://www.geeksforgeeks.org/sending-emails-using-api-in-flask-mail/
#gmail:  study.groupmatching@gmail.com
#password: 7pKsm'v~.T=xTe9/]
mail = Mail(app) # instantiate the mail class


# Guarantees templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'study.groupmatching@gmail.com'
app.config['MAIL_PASSWORD'] = "7pKsm'v~.T=xTe9/]"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# sets up users database 
db = SQL("sqlite:///users.db")

# message object mapped to a particular URL ‘/’
# recipients = a list of strings of the group members' emails 
# course = course name, day = the day the study group will meet
# time = the time the study group will meet 
# location = a dictionary of the different locations that members of 
# the study group prefer, each key being a different location and 
# each value being the corresponding percentage of study group members
# who prefer that location

@app.route("/register")
def register(): 
    return render_template("register.html")
@app.route("/login")
def index(): 
    return render_template("login.html")

@app.route("/calendar")
@login_required
def calendar(): 
    return render_template("calendar.html")

@app.route("/")
@login_required
def home(): 
    return render_template("main.html")

@app.route("/prefs", methods=["GET", "POST"])
@login_required
def prefs(): 
    locations = ["Cabot Library", "Dorm Room", "Lamont Library", "Smith Center", "Widener Library"]
    if request.method == "POST":
        '''Assume that course is the course they enter into the form
        Assume that size is the size preference they enter into the form
        Assume that timelist is the comma separated list of times that we create from the times they enter into the form
        Assume that locationlist is the comma separrated list of locations that we create from the locations they enter into the form
        
        table = db.execute("SELECT course FROM preferences WHERE email = ? AND course = ?", email, course)
        try:
            if len(table[0]['courses'] > 0):
                db.execute("UPDATE preferences SET size = ?, times = ?, locations = ? WHERE email = ? AND course = ?, size, timelist, locationlist, email, course)
            else:
                db.execute("INSERT INTO preferences (email, course, size, times, locations) VALUES (?, ?, ?, ?, ?)", email, course, size, timelist, locationlist)
        except: 
            db.execute("INSERT INTO preferences (email, course, size, times, locations) VALUES (?, ?, ?, ?, ?)", email, course, size, timelist, locationlist)
        
        Matching algorithm: 
        courses = db.execute("SELECT DISTINCT course FROM preferences")
        for course in courses: 
            #first course is variable name, second course is in for loop, third course refers to course entry in table
            course = course["course"]
            same_courses = db.execute("SELECT * FROM preferences WHERE course = ?", course)
            
            
            
        '''
        #location = request.form.get("location")
        return render_template("prefs.html")

    if request.method == "GET":

        return render_template("prefs.html", locations=locations)

def matchemail(recipients, course, day, time, location):
    for i in range(len(recipients)):      
        msg = Message(
                    #Problem: Gets marked as spam
                    'Hello',
                    sender ='study.groupmatching@gmail.com',
                    #Problem: Recipients can see all other recipients (not BCC)
                    #solution: https://stackoverflow.com/questions/1546367/python-how-to-send-mail-with-to-cc-and-bcc
                    recipients = ['arjunfeb1803@gmail.com', 'edwardkang@college.harvard.edu']
                    )
                    #string formatting in python: https://realpython.com/python-string-formatting/
        t = Template('Hello, $name. You have been matched! Your study group for $course will meet $day at $time. ')
        for x in location: 
            t += "\n" + location[x] + "% of the group prefer " + x
        t.substitute(name=recipients[i], course=course, day=day, time=time)
        msg.body(t)
        mail.send(msg)
        return 'Sent'
def verify(): 
    msg = Message(
                'study.group Email Verification',
                sender ='study.groupmatching@gmail.com',
                recipients = ['edwardkang@college.harvard.edu']
               )
    msg.body = '#Hello [name] You have been matched! Your study group for [class] will meet [day] at [time] Here are your groupmates! [name, email] [name, email] etc.'
    mail.send(msg)
    return 'Sent'
if __name__ == '__main__':
   app.run(debug = True)



# rough draft of the schema for the SQL database storing users' info
# each row will have an email address, an array of courses, an array of arrays of times where the user is available, 
# 
