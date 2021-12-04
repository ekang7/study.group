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

# dictionary that serves as a converter between times and indices 
time_to_index = {
                    "12:00am": 0,
                    "12:15am": 1,
                    "12:30am": 2,
                    "12:45am": 3, 
                    "1:00am": 4, 
                    "1:15am": 5,
                    "1:30am": 6, 
                    "1:45am": 7,
                    "2:00am": 8, 
                    "2:15am": 9,
                    "2:30am": 10,
                    "2:45am": 11,
                    "3:00am": 12,
                    "3:15am": 13,
                    "3:30am": 14,
                    "3:45am": 15, 
                    "4:00am": 16,
                    "4:15am": 17,
                    "4:30am": 18,
                    "4:45am": 19,
                    "5:00am": 20,
                    
                    "6:15am": 21, 
                    "6:30am": 22,
                    "6:45am": 23,
                    "7:00am": 24,
                    "7:15am": 25,
                    "7:30am": 26,
                    "7:45am": 27,
                    "8:00am": 28, 
                    "8:15am": 29,
                    "8:30am": 30,
                    "8:45am": 31, 
                    "9:00am": 32, 
                    "9:15am": 33, 
                    "9:30am": 34, 
                    "9:45am": 35, 
                    "10:00am": 36, 
                    "10:15am": 37,
                    "10:30am": 38,
                    "10:45am": 39,
                    "11:00am": 40,
                    "11:15am": 41, 
                    "11:30am": 42, 
                    "11:45am": 43,
                    "12:00pm": 44, 
                    "12:15pm": 45,
                    "12:30pm": 46,
                    "12:45pm": 47,
                    "1:00pm": 48,
                    "1:15pm": 49,
                    "1:30pm": 50,
                    "1:45pm": 51, 
                    "2:00pm": 52, 
                    "2:15pm": 53, 
                    "2:30pm": 54, 
                    "2:45pm": 55, 
                    "3:00pm": 56, 
                    "3:15pm": 57,
                    "3:30pm": 58, 
                    "3:45pm": 59, 
                    "4:00pm": 60, 
                    "4:15pm": 61, 
                    "4:30pm": 62, 
                    "4:45pm": 63, 
                    "5:00pm": 64, 
                    "6:15pm": 65, 
                    "6:30pm": 66, 
                    "6:45pm": 67, 
                    "7:00pm": 68, 
                    "7:15pm": 69, 
                    "7:30pm": 70, 
                    "7:45pm": 71, 
                    "8:00pm": 72, 
                    "8:15pm": 73, 
                    "8:30pm": 74, 
                    "8:45pm": 75, 
                    "9:00pm": 76, 
                    "9:15pm": 77, 
                    "9:30pm": 78, 
                    "9:45pm": 79, 
                    "10:00pm": 80, 
                    "10:15pm": 81, 
                    "10:30pm": 82, 
                    "10:45pm": 83, 
                    "11:00pm": 84, 
                    "11:15pm": 85, 
                    "11:30pm": 86, 
                    "11:45pm": 87, 
} 

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

def match(): 
    # Runs timematch on every unique course in the prefs table
    uniqueCourses = db.execute("SELECT DISTINCT course FROM prefs;")
    for uniqueCourse in uniqueCourses: 
        timematch(uniqueCourse["course"])
def timematch(uniqueCourse): 
    # stackedTimelines stores how many people are available at each time represented by each index of 
    # stackedTimelines 
    # assume 
    stackedTimelines = [0] * 96
    timelines = db.execute("SELECT times FROM prefs WHERE course = ?", uniqueCourse)
    
def grouper():
    # TODO
    return 0
if __name__ == '__main__':
   app.run(debug = True)



# rough draft of the schema for the SQL database storing users' info
# each row will have an email address, an array of courses, an array of arrays of times where the user is available, 
# 
