# Implements a registration form, confirming registration via email

import os
import re

from flask import Flask, render_template, request
from flask_mail import Mail, Message
from string import Template

app = Flask(__name__)
# template for email code from https://www.geeksforgeeks.org/sending-emails-using-api-in-flask-mail/
#gmail:  study.groupmatching@gmail.com
#password: 7pKsm'v~.T=xTe9/]
mail = Mail(app) # instantiate the mail class
   
# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'study.groupmatching@gmail.com'
app.config['MAIL_PASSWORD'] = "7pKsm'v~.T=xTe9/]"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
   
# message object mapped to a particular URL ‘/’
# recipients = a list of strings of the group members' emails 
# course = course name, day = the day the study group will meet
# time = the time the study group will meet 
# location = a dictionary of the different locations that members of 
# the study group prefer, each key being a different location and 
# each value being the corresponding percentage of study group members
# who prefer that location  
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
                recipients = ['arjunfeb1803@gmail.com']
               )
    msg.body = '#Hello [name] You have been matched! Your study group for [class] will meet [day] at [time]Here are your groupmates! [name, email] [name, email] etc.'
    mail.send(msg)
    return 'Sent'
if __name__ == '__main__':
   app.run(debug = True)



# rough draft of the schema for the SQL database storing users' info
# each row will have an email address, an array of courses, an array of arrays of times where the user is available, 
# 