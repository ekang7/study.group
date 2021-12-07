# Implements a registration form, confirming registration via email

import os
import re
from cs50 import SQL
from flask import Flask, render_template, request, session, url_for, redirect
from flask_mail import Mail, Message
from string import Template
from flask_session import Session
from login import login_required
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer

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

daysoftheweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
# dictionary that serves as a converter between times and indices 
time_to_index = {
                    "12:00am": 0,
                    "12:30am": 1,
                    "1:00am": 2,
                    "1:30am": 3, 
                    "2:00am": 4, 
                    "2:30am": 5,
                    "3:00am": 6, 
                    "3:30am": 7,
                    "4:00am": 8, 
                    "4:30am": 9,
                    "5:00am": 10,
                    "5:30am": 11,
                    "6:00am": 12,
                    "6:30am": 13,
                    "7:00am": 14,
                    "7:30am": 15, 
                    "8:00am": 16,
                    "8:30am": 17,
                    "9:00am": 18,
                    "9:30am": 19,
                    "10:00am": 20,
                    "10:30am": 21,
                    "11:00am": 22,
                    "11:30am": 23,
                    "12:00pm": 24,
                    "12:30pm": 25, 
                    "1:00pm": 26,
                    "1:30pm": 27,
                    "2:00pm": 28,
                    "2:30pm": 29,
                    "3:00pm": 30,
                    "3:30pm": 31,
                    "4:00pm": 32, 
                    "4:30pm": 33,
                    "5:00pm": 34,
                    "5:30pm": 35, 
                    "6:00pm": 36, 
                    "6:30pm": 37, 
                    "7:00pm": 38, 
                    "7:30pm": 39, 
                    "8:00pm": 40, 
                    "8:30pm": 41,
                    "9:00pm": 42,
                    "9:30pm": 43,
                    "10:00pm": 44,
                    "10:30pm": 45, 
                    "11:00pm": 46, 
                    "11:30pm": 47
} 

# message object mapped to a particular URL ‘/’
# recipients = a list of strings of the group members' emails 
# course = course name, day = the day the study group will meet
# time = the time the study group will meet 
# location = a dictionary of the different locations that members of 
# the study group prefer, each key being a different location and 
# each value being the corresponding percentage of study group members
# who prefer that location

#Creates a password salt
SECURITY_PASSWORD_SALT = 'v6u9-DwrC@BL'

@app.route("/register", methods = ["GET", "POST"])
def register(): 
    if request.method == "POST":
        error = ""
        email = request.form.get("email")
        firstname = request.form.get("firstName")
        lastname = request.form.get("lastName")
        password = request.form.get("password")
        passwordconfirm = request.form.get("confirmation")
        if not email or not password or not firstname or not lastname:
        #if len(email) == 0 or len(password) == 0 or len(firstname) ==0 or len(lastname ==0):
            error = "All fields must be filled out"
            return render_template("register.html",error=error)
        else:
            if len(db.execute("SELECT * FROM users WHERE email = ?", email)) > 0:
                error = "There is an account associated with this email"
                return render_template("register.html",error=error)
            else:
                if password != passwordconfirm:
                    error = "Please make sure your confirmation matches your password"
                    return render_template("register.html",error=error)
                else:
                    passwordhash = generate_password_hash(password)
                    db.execute("INSERT INTO users (email, password, firstname, lastname) VALUES(?, ?, ?, ?)", email, passwordhash, firstname, lastname)
                   # verify(email, firstname)
                    return render_template("login.html", errormessage = "WELCOME!")
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def index():
    session.clear()

    if request.method == "POST":
        # check if email was submitted
        if not request.form.get("email"):
            return render_template("login.html", errormessage = "Please enter an email!")
        # check if password was submitted
        if not request.form.get("password"):
            return render_template("login.html", errormessage = "Please enter a password!")
         
        # query for the given email from user table
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        # check if email is a user and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            errormessage = "Incorrect login"
            return render_template("login.html", errormessage = errormessage)
        
        # remember user
        session["user_id"] = rows[0]["email"]
        # redirect to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/")
def home(): 
    return render_template("main.html")
    

@app.route("/prefs", methods=["GET", "POST"])
def prefs(): 
    locations = ["Cabot Library", "Dorm Room", "Lamont Library", "Smith Center", "Widener Library"]
    userprefs = db.execute("SELECT * FROM prefs WHERE email = ? ", session["user_id"])
    # [
    #  [courses]
    # [timeDict]
    # [groupsizes]
    # [locations]
    # ]
    #if userprefs: 
        #courses = a list of all courses, timeDict, locations, group size
     #   coursesprefs = []
      #  counter = 0 
       # for x in userprefs: 
        #    coursesprefs.append({})
         #   coursesprefs[counter]["course"] = 

    if request.method == "POST":
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        #Assume that course is the course they enter into the form
        #Assume that size is the size preference they enter into the form
        #Assume that timelist is the comma separated list of times that we create from the times they enter into the form
        #Assume that locationlist is the comma separrated list of locations that we create from the locations they enter into the form
        #the timelist should be times from least to greatest, CHECK IF THIS IS AUTOMATICALLY DONE 
        course = request.form.get("course")
        email = session["user_id"]
        #day = request.form.get("day")
        size = request.form.get("size")
        locationlist = request.form.get("location")
        timeDict = {}
        #https://stackoverflow.com/questions/12502646/access-multiselect-form-field-in-flask
        for x in daysoftheweek: 
            timeDict[x] = request.form.getlist(x)
            timestring = ""
            for y in timeDict[x]: 
                timestring += y +","
            timestring = timestring[0:len(timestring)-1]
            timeDict[x] = timestring
            print(timeDict[x])
            table = db.execute("SELECT course FROM prefs WHERE email = ? AND course = ? AND day = ?", email, course, x)
            try:
                if len(table[0]['course']) > 0:
                    db.execute("UPDATE prefs SET size = ?, times = ?, locations = ? WHERE email = ? AND course = ? AND day = ?", size, timeDict[x], locationlist, email, course, x)
                else:
                    db.execute("INSERT INTO prefs (email, course, size, times, locations, day) VALUES (?, ?, ?, ?, ?, ?)", email, course, size, timeDict[x], locationlist, x)
            except:
                db.execute("INSERT INTO prefs (email, course, size, times, locations, day) VALUES (?, ?, ?, ?, ?, ?)", email, course, size, timeDict[x], locationlist, x)
        
        #Matching algorithm: 
        #courses = db.execute("SELECT DISTINCT course FROM prefs")
        #for course in courses: 
            #first course is variable name, second course is in for loop, third course refers to course entry in table
            #course = course["course"]
            #same_courses = db.execute("SELECT * FROM prefs WHERE course = ?", course)
            
            
            
        
        #location = request.form.get("location")
        return render_template("prefs.html", locations = locations, daysoftheweek = daysoftheweek, time_to_index = time_to_index)

    else:
       
        return render_template("prefs.html", locations=locations, daysoftheweek = daysoftheweek, time_to_index = time_to_index)

def matchemail(people, locations, timeblock, day, uniqueCourse, matched):
    #people as a list
    #locations as a dictionary
    #uniquecourse as a integer valiue
    #matched as a boolean
    # day is one day because we are only matching for one day per week
    print("LOOOOOOOOOOOOK")
    print(people)
    count = len(people)
    if not matched:
        timesdictSunday={}
        timesdictMonday={}
        timesdictTuesday={}
        timesdictWednesday = {}
        timesdictThursday = {}
        timesdictFriday = {}
        timesdictSaturday = {}
        fulllistoftimes =[timesdictSunday,timesdictMonday, timesdictTuesday, timesdictWednesday, timesdictThursday, timesdictFriday, timesdictSaturday]
        daycount = 0
        for aday in daysoftheweek:
            timesdict = fulllistoftimes[daycount]
            for person in people: 
                timetable = db.execute("SELECT times FROM prefs WHERE email LIKE ? AND course = ? AND day = ?", person, uniqueCourse, aday)
                timelist = timetable['times'].split(",")
                for entry in timelist:
                    if timesdict.has_key(entry):
                        timesdict[entry] = timesdict[entry] + 1
                    else:
                        timesdict[entry] = 1

            for entry in timesdict:
                timesdict[entry] = timesdict[entry]/count
            daycount = daycount + 1
        timetext = ""
        for x in range(7):
            timesdict = fulllistoftimes[x]
            for entry in timesdict:
                if timesdict.has_key(entry):
                    timetext = timetext + timetext[entry] + " of people prefer " + entry + " on " + daysoftheweek[x] + ". "
        locationtext = ""
        for entry in locations:
            locationtext = locationtext + locations[entry]/count + " of people prefer " + entry + ". "
        names = ""
        for person in people:
            if names == "":
                names = db.execute("SELECT firstname from users WHERE email = ?", person)['firstname']
            else:
                names = names + ", " + db.execute("SELECT firstname from users WHERE email = ?", person)['firstname']

        msg = Message(
                    'An Update on Your Study Group!',
                    sender ='study.groupmatching@gmail.com',
                    #Problem: Recipients can see all other recipients (not BCC)
                    #solution: https://stackoverflow.com/questions/1546367/python-how-to-send-mail-with-to-cc-and-bcc
                    recipients = people
                    )
                    #string formatting in python: https://realpython.com/python-string-formatting/
        
        t = Template('Hello, $name. Unfortunately, we were not able to find a perfect match for you for $course. Nevertheless, we are sending a list of preferred times and locations for other people in your class who need a group: ')
        t.replace('$name', names)
        t.replace('$course', uniqueCourse)
        t = t + timetext
        t = t+ locationtext
        msg.body(t)
        mail.send(msg)
        return 'Sent'

    if matched:
        locationtext = ""
        for entry in locations:
            locationtext = locationtext + locations[entry]/count + " of people prefer " + entry + ". "

        for person in people:
            if names == "":
                names = db.execute("SELECT firstname from users WHERE email = ?", person)['firstname']
            else:
                names = names + ", " + db.execute("SELECT firstname from users WHERE email = ?", person)['firstname']

        msg = Message(
                    'You have been matched!',
                    sender ='study.groupmatching@gmail.com',
                    recipients = people
                    )
                    #string formatting in python: https://realpython.com/python-string-formatting/
        
        t = Template('Hello, $name. We wanted to let you know that you have been matched! Your group for $course will meet on $day at $time.')
        t.replace('$name', names)
        t.replace('$course', uniqueCourse)
        t.replace('$day', day)
        t.replace('$time', timeblock)
        t = t + locationtext
        msg.body(t)
        mail.send(msg)
        return 'Sent'
#Code for generating and confirming token taken from https://realpython.com/handling-email-confirmation-in-flask/#generate-confirmation-token
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer('SECRET_KEY')
    return serializer.dumps(email, salt='SECURITY_PASSWORD_SALT')


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer('SECRET_KEY')
    try:
        email = serializer.loads(
            token,
            salt='SECURITY_PASSWORD_SALT',
            max_age=expiration
        )
    except:
        return False
    return email

def verify(email, firstname): 
    token = generate_confirmation_token(email)
    confirm_url = url_for(email, token=token, _external=True)
    msg = Message(
                'study.group Email Verification',
                sender ='study.groupmatching@gmail.com',
                recipients = email
               )
    t = "#Hello, $name! Thank you for registering for study.group! To complete your registration, please click the following link: $link"
    t = t.replace('$name', firstname)
    t = t.replace('$link', confirm_url)
    msg.body = t
    mail.send(msg)
    return 'Sent'
    
def match(): 
    # Creates copy of preferences table called prefs to save preferences information
  #  db.execute("SELECT * INTO prefs FROM preferences;")  
   # db.execute("ALTER TABLE prefs ADD matched bit")
    #db.execute("UPDATE prefs SET matched = ?", 0)
    # Runs timematch on every unique course in the prefs table
    uniqueCourses = db.execute("SELECT DISTINCT course FROM prefs;")
    for uniqueCourse in uniqueCourses: 
        for day in daysoftheweek:
            timematch(uniqueCourse["course"], day)
    # Deal with leftover people by course and by day
    for uniqueCourse in uniqueCourses:
        for day in daysoftheweek:
            # List of emails of unmatched people with given course and day
            people = []
            # dictionary of count of preferred locations of all people with given course and day
            locations = {
                "Cabot Library": 0, 
                "Dorm Room": 0, 
                "Lamont Library": 0, 
                "Smith Center": 0, 
                "Widener Library": 0
            }
            leftovers = db.execute("SELECT * FROM prefs WHERE course = ?", uniqueCourse["course"])
            if not leftovers: 
                for leftover in leftovers:
                    people.append(leftover["email"])
                    locationPrefs = leftover["locations"]
                    for locationPref in locationPrefs:
                        locations[locationPref] = locations[locationPref] + 1
                matchemail(people, locations, None, None, uniqueCourse["course"], 0)

# prereq = the sorting has already been filtered by course 
def timematch(uniqueCourse, day): 
    # stackedTimelines stores how many people are available at each time represented by each index of 
    # stackedTimelines 
    # assume 
    stackedTimelines = [0] * 48
    timelines = db.execute("SELECT times FROM prefs WHERE course = ? AND day = ?", uniqueCourse, day)
    #https://www.kite.com/python/answers/how-to-convert-a-comma-separated-string-to-a-list-in-python#:~:text=Use%20str.,separated%20string%20into%20a%20list.
    for timeline in timelines: 
        timeline = timeline["times"]
        timelist = timeline.split(",")
        # timeline has been split into a list of times 
        #https://www.kite.com/python/answers/how-to-remove-empty-strings-from-a-list-of-strings-in-python
        filteredtimelist = filter(lambda x: x != "", timelist)
        timelist = list(filteredtimelist)
        for time in timelist: 
            stackedTimelines[time_to_index[time]] += 1


    # now stackedtimelines has the number of people who want a specific course at each time block 
    # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/   
    sortedStackedTimelines = sorted(stackedTimelines.items(), key=lambda x: x[1], reverse=True)
    # Now stackedTimelines is sorted according by popularity of time and stored as a dictionary in sortedStackedTimelines
    # https://realpython.com/iterate-through-dictionary-python/
    stackedTimelinesKeys = stackedTimelines.keys()
    stackedTimelinesValues = stackedTimelines.values()
    for key in sortedStackedTimelines: 
        max_value = sortedStackedTimelines[key]
        if max_value == 0: 
            break
        # finds 30 minute blocks with max people 
        # https://www.programiz.com/python-programming/methods/list/index
        timeblock = []
        am_timeblock = []
        pm_timeblock = []
        max_index = stackedTimelinesKeys.index(key)
        peopledict = db.execute("SELECT email FROM prefs WHERE course = ? AND times LIKE %?% AND day = ?;", uniqueCourse, key, day)
        people = []
        for x in peopledict: 
            people.append(x["email"])
        # now we have the list of people who the most popular 30 minute block works with
        # we wil now look to before and after this 30 minute block to see if the same people are available for a longer
        # block of time 
        if key[len(key)-2] == "am":
            am_timeblock.append(key)
        else: 
            pm_timeblock.append(key)
        for left in range(max_index-1, -1, -1):
            key2 = stackedTimelinesKeys[left]
            peopledict2 = db.execute("SELECT email FROM prefs WHERE course = ? AND times LIKE %?% AND day = ?;", uniqueCourse, key2, day)
            people2 = []
            for x in peopledict2: 
                people2.append(x["email"]) 
            #https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/#:~:text=Check%20if%20list1%20contains%20all%20elements%20of%20list2%20using%20all()&text=Python%20all()%20function%20checks,if%20element%20exists%20in%20list1.
            contained =  all(elem in people2  for elem in people)
            if not contained:
                break
            else: 
                 if key[len(key2)-2] == "am":
                    am_timeblock.append(key2)
                 else: 
                    pm_timeblock.append(key2)
        for right in range(max_index, len(stackedTimelinesKeys)):
            key2 = stackedTimelinesKeys[right]
            peopledict2 = db.execute("SELECT email FROM prefs WHERE course = ? AND times LIKE %?% AND day = ?;", uniqueCourse, key2, day)
            people2 = []
            for x in peopledict2: 
                people2.append(x["email"]) 
            #https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/#:~:text=Check%20if%20list1%20contains%20all%20elements%20of%20list2%20using%20all()&text=Python%20all()%20function%20checks,if%20element%20exists%20in%20list1.
            contained =  all(elem in people2  for elem in people)
            if not contained:
                break
            else: 
                 if key[len(key2)-2] == "am":
                    am_timeblock.append(key2)
                 else: 
                    pm_timeblock.append(key2)
        am_timeblock.sort()
        pm_timeblock.sort()
        timeblock = am_timeblock+pm_timeblock
        grouped_people = grouper(uniqueCourse, timeblock, people, day)
    # Handle left over people
    

# prereq = the sorting has already been filtered by course and time 
# Grouping algorithm for people for a particular time interval by group size 
def grouper(uniqueCourse, timeblock, emails, day):
    timestring = ""
    locationstring = ""
    for time in timeblock: 
        timestring += time + ","
    course_entries = db.execute("SELECT * FROM prefs WHERE course = ? and times LIKE %?% AND day = ?", uniqueCourse, timestring, day)
    for course_entry in course_entries: 
        locationstring += course_entry["locations"] + ","
    number_of_people = len(course_entries)
    if number_of_people <= 3:
        matchemail(emails, locationstring, timeblock, day, uniqueCourse, True)
        db.execute("UPDATE prefs SET matched = 1 WHERE course = ? AND times LIKE %?% AND day = ?", uniqueCourse, timestring, day)    
    elif number_of_people <=6 and number_of_people >=4:
       large = sizeCount(course_entries, "l")
       medium = sizeCount(course_entries, "m")
       small = number_of_people - large - medium  
       if small > (medium + large): 
           #remainder = number_of_people % 3
           #if remainder == 0: 
           #     matchemail(emails[], locationstring, timeblock, day, uniqueCourse, True)
           #elif remainder == 1: 
           #else: 
           if number_of_people == 4: 
               matchemail(emails[0:2], locationstring, timeblock, day, uniqueCourse, True)
               matchemail(emails[2:4], locationstring, timeblock, day, uniqueCourse, True)
           elif number_of_people == 5: 
               matchemail(emails[0:2], locationstring, timeblock, day, uniqueCourse, True)
               matchemail(emails[3:5], locationstring, timeblock, day, uniqueCourse, True)
           else: 
               matchemail(emails[0:3], locationstring, timeblock, day, uniqueCourse, True)
               matchemail(emails[4:6], locationstring, timeblock, day, uniqueCourse, True)
       else:
           matchemail(emails, locationstring, timeblock, day, uniqueCourse, True)
       db.execute("UPDATE prefs SET matched = 1 WHERE course = ? AND times LIKE %?% AND day = ?", uniqueCourse, timestring, day) 
    else: # 7+ people
       large = sizeCount(course_entries, "l")
       medium = sizeCount(course_entries, "m")
       small = number_of_people - large - medium
       large_people_dict = db.execute("SELECT email FROM prefs WHERE course = ? AND timeblock LIKE %?% AND day = ? AND size = ?", uniqueCourse, timeblock, day, "l")
       large_people = []
       for t in large_people_dict: 
           large_people.append(large_people_dict["email"])
       medium_people_dict = db.execute("SELECT email FROM prefs WHERE course = ? AND timeblock LIKE %?% AND day = ? AND size = ?", uniqueCourse, timeblock, day, "m")
       medium_people = []
       for t in medium_people_dict: 
           medium_people.append(medium_people_dict["email"])
       small_people_dict = db.execute("SELECT email FROM prefs WHERE course = ? AND timeblock LIKE %?% AND day = ? AND size = ?", uniqueCourse, timeblock, day, "s")
       small_people = []
       for t in small_people_dict:
           small_people.append(small_people_dict["email"])
       if small == 1:
            medium = medium + small
            small = 0
            #change the person's categorization in the table to medium
            #db.execute("UPDATE prefs SET size = ? WHERE course = ? AND size = ? AND day = ? AND times LIKE %?%;","m", uniqueCourse, "s", day, timestring)
            medium_people.append(small_people.pop())
       s = small

       if number_of_people - s < 4:
            s = number_of_people - 4
       smallbutnots = small - s
       medium = medium + smallbutnots
       for x in range(smallbutnots):
           medium_people.append(small_people.pop())
      # db.execute("UPDATE prefs SET size = ? WHERE course = ? AND size = ? AND day = ? AND times LIKE %?%;")
       remainder = s % 3
       if remainder == 0: 
       # all groups of 3
            for i in range(0, s, 3):
                matchemail(small_people[i:i+3], locationstring, timeblock, day, uniqueCourse, True)
       elif remainder == 1:
           # 2 groups of 2, rest is group of 3
            matchemail(small_people[0,2], locationstring, timeblock, day, uniqueCourse, True)
            matchemail(small_people[2,4], locationstring, timeblock, day, uniqueCourse, True)
            for i in range(4, s, 3):
                matchemail(small_people[i:i+3], locationstring, timeblock, day, uniqueCourse, True)

       else: 
        # 1 group of 2, rest is group of 3
            matchemail(small_people[0,2], locationstring, timeblock, day, uniqueCourse, True)
            for i in range(2,s,3):
                 matchemail(small_people[i:i+3], locationstring, timeblock, day, uniqueCourse, True)
     
       #All unmatched small people are moved to medium
       if large < 7:
            medium = medium + large
            large = 0
            for x in large: 
                medium_people.append(large_people.pop())
            #change the large people's categorization to medium
            #db.execute("UPDATE prefs SET size = ? WHERE course = ? AND size = ? AND day = ? AND times LIKE %?%;", "m", uniqueCourse, "l", day, timestring)
       if large >= 7:
            remainder = large%7
            number_of_largegroups = (large-remainder)/7
            #If large is 7-13, they are all together. If large is 14-20, form two large groups, etc. for multiples of 7
            for i in range(0, number_of_largegroups * 7 -7, 7):
                matchemail(large_people[i:i+7], locationstring, timeblock, day, uniqueCourse, True)
            matchemail(large_people[len(large_people)-remainder - 7:len(large_people)], locationstring, timeblock, day, uniqueCourse, True)
       m = medium
       remainder = m%6
       if remainder == 0:
            #all medium groups of 6
            for i in range(0, s, 6):
                matchemail(medium_people[i:i+6], locationstring, timeblock, day, uniqueCourse, True)
       elif remainder == 1:
            #one medium group of 7, the rest is all groups of 6
            matchemail(medium_people[0:7], locationstring, timeblock, day, uniqueCourse, True)
            for i in range(7, s, 6):
                matchemail(medium_people[i:i+6], locationstring, timeblock, day, uniqueCourse, True)
       elif remainder == 2:
            #two medium groups of 4, the rest is all groups of 6
            matchemail(medium_people[0:4], locationstring, timeblock, day, uniqueCourse, True)
            matchemail(medium_people[4:8], locationstring, timeblock, day, uniqueCourse, True)
            for i in range(8, s, 6):
                matchemail(medium_people[i:i+6], locationstring, timeblock, day, uniqueCourse, True)
       elif remainder == 3:
           #medium group of 4, medium group of 5, the rest is all groups of 6
           matchemail(medium_people[0:4], locationstring, timeblock, day, uniqueCourse, True)
           matchemail(medium_people[4:9], locationstring, timeblock, day, uniqueCourse, True)
           for i in range(9, s, 6):
                matchemail(medium_people[i:i+6], locationstring, timeblock, day, uniqueCourse, True)
       elif remainder == 4:
            #medium group of 4, the rest is all groups of 6
            matchemail(medium_people[0:4], locationstring, timeblock, day, uniqueCourse, True)
            for i in range(4, s, 6):
                matchemail(medium_people[i:i+6], locationstring, timeblock, day, uniqueCourse, True)
       else:
       #medium group of 5, the rest is all groups of 6
            matchemail(medium_people[0:5], locationstring, timeblock, day, uniqueCourse, True)
            for i in range(5, s, 6):
                matchemail(medium_people[i:i+6], locationstring, timeblock, day, uniqueCourse, True)

    return 0

# returns the number of people who chose "size" pref in course_entries
def sizeCount(course_entries, size):
    count = 0   
    for course_entry in course_entries: 
        if course_entry["size"] == size: 
            count += 1
    return count


if __name__ == '__main__':
   app.run(debug = True)
match()
       
        
    
# rough draft of the schema for the SQL database storing users' info
# each row will have an email address, an array of courses, an array of arrays of times where the user is available, 
# 



    