# Introducing...study.group!

import os
import re
from cs50 import SQL
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mail import Mail, Message
from string import Template
from flask_session import Session
from login import login_required
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
# Template for email code from https://www.geeksforgeeks.org/sending-emails-using-api-in-flask-mail/
# Instantiates the mail class
mail = Mail(app) 


# Guarantees templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configuration of mail
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

# Sets up users database 
db = SQL("sqlite:///users.db")

# List of days of the week 
daysoftheweek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Dictionary that serves as a converter between times and indices 
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

# The same thing, but in reverse!
index_to_time = {
                    0: "12:00am",
                    1: "12:30am",
                    2: "1:00am",
                    3: "1:30am",
                    4: "2:00am", 
                    5: "2:30am",
                    6: "3:00am",
                    7: "3:30am",
                    8: "4:00am",
                    9: "4:30am",
                    10: "5:00am",
                    11: "5:30am",
                    12: "6:00am",
                    13: "6:30am",
                    14: "7:00am",
                    15: "7:30am",
                    16: "8:00am",
                    17: "8:30am",
                    18: "9:00am",
                    19: "9:30am",
                    20: "10:00am",
                    21: "10:30am",
                    22: "11:00am",
                    23: "11:30am",
                    24: "12:00pm",
                    25: "12:30pm",
                    26: "1:00pm",
                    27: "1:30pm",
                    28: "2:00pm",
                    29: "2:30pm",
                    30: "3:00pm",
                    31: "3:30pm",
                    32: "4:00pm",
                    33: "4:30pm",
                    34: "5:00pm",
                    35: "5:30pm",
                    36: "6:00pm",
                    37: "6:30pm",
                    38: "7:00pm",
                    39: "7:30pm",
                    40: "8:00pm",
                    41: "8:30pm",
                    42: "9:00pm",
                    43: "9:30pm",
                    44: "10:00pm",
                    45: "10:30pm",
                    46: "11:00pm",
                    47: "11:30pm"
} 

# Handles user registration
@app.route("/register", methods = ["GET", "POST"])
def register(): 
    if request.method == "POST":
        # Error is sent to the template to show what error may pop up when registering (its default value is "" signifying no error)
        error = ""
        # Take information entered by the user during registration and store as variables
        email = request.form.get("email")
        firstname = request.form.get("firstName")
        lastname = request.form.get("lastName")
        password = request.form.get("password")
        passwordconfirm = request.form.get("confirmation")
        # Ensure that all fields are filled out
        if not email or not password or not firstname or not lastname:
            error = "All fields must be filled out"
            return render_template("register.html",error=error)
        else:
            # Check if there is an account already associated with the email
            if len(db.execute("SELECT * FROM users WHERE email = ?", email)) > 0:
                error = "There is an account associated with this email"
                return render_template("register.html",error=error)
            else:
                # Make sure that the password is the same as their password confirmation
                if password != passwordconfirm:
                    error = "Please make sure your confirmation matches your password"
                    return render_template("register.html",error=error)
                else:
                    # Store the user's information and a hash of their password in the users database 
                    passwordhash = generate_password_hash(password)
                    db.execute("INSERT INTO users (email, password, firstname, lastname) VALUES(?, ?, ?, ?)", email, passwordhash, firstname, lastname)
                    # Once they have successfully registered, welcome the user and direct them to login!
                    return render_template("login.html", errormessage = "WELCOME!")
    else:
        # Return the register page
        return render_template("register.html")


# Handles user login 
@app.route("/login", methods=["GET", "POST"])
def index():
    session.clear()

    if request.method == "POST":
        # Check if email was submitted
        if not request.form.get("email"):
            return render_template("login.html", errormessage = "Please enter an email!")
        # Check if password was submitted
        if not request.form.get("password"):
            return render_template("login.html", errormessage = "Please enter a password!")
         
        # Query for the given email from user table
        rows = db.execute("SELECT * FROM users WHERE email = ?", request.form.get("email"))
        # Check if email is a user and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            errormessage = "Incorrect login"
            return render_template("login.html", errormessage = errormessage)

        # Remember user
        session["user_id"] = rows[0]["email"]
        # Redirect to home page
        return redirect("/")

    else:
        # Return the login page
        return render_template("login.html")

# Handles user logout 
@app.route("/logout")
@login_required
def logout():
    # Previously defined in the Finance problem set
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/courses", methods=["GET", "POST"])
@login_required
def courses(): 
    if request.method == "POST":
        # Take the course, resourcelink, and resourcetitle for the resource the user is submitting
        course = request.form.get('resourceCourse')
        resourcelink = request.form.get("resourceLink")
        resourcetitle = request.form.get("resourceTitle")
        print(course)
        print(resourcelink)
        print(resourcetitle)
        # Insert values into the courses table
        db.execute("INSERT INTO courses (course, url, title) VALUES (?, ?, ?)", course, resourcelink, resourcetitle)
        # Find all the courses that the current logged in user has submitted preferences for
        coursesDict = db.execute("SELECT DISTINCT course FROM prefs WHERE email = ?", session["user_id"])
        courses = []
        for courseDict in coursesDict: 
            courses.append(courseDict["course"])
        resources = {} 
        # Find all the resources associated with the courses the user has submitted preferences for
        for course in courses:
           tempDict = db.execute("SELECT title, url FROM courses WHERE course = ?;", course)
           for temp in tempDict:
                try:
                    resources[course] = resources[course] + [temp["title"], temp["url"]]
                except: 
                    resources[course] = [temp["title"], temp["url"]]
        # Return the courses page with the list of courses the user has submitted preferences for, and the corresponding resources
        return render_template("courses.html", courses = courses, resources = resources)
    else: 
        # Find all the courses that the current logged in user has submitted preferences for
        coursesDict = db.execute("SELECT DISTINCT course FROM prefs WHERE email = ?", session["user_id"])
        courses = []
        for courseDict in coursesDict: 
            courses.append(courseDict["course"])
        resources = {} 
        # Find all the resources associated with the courses the user has submitted preferences for
        for course in courses:
            tempDict = db.execute("SELECT title, url FROM courses WHERE course = ?;", course)
            for temp in tempDict:
                try:
                    resources[course] = resources[course] + [temp["title"], temp["url"]]
                except: 
                    resources[course] = [temp["title"], temp["url"]]
         # Return the courses page with the list of courses the user has submitted preferences for, and the corresponding resources
        return render_template("courses.html", courses = courses, resources = resources) 

# Set the homepage for our website to "main.html"
@app.route("/")
def home(): 
    return render_template("main.html")

@app.route("/prefs", methods=["GET", "POST"])
@login_required
def prefs(): 
    # List of locations that we want people to be able to select from when submitting preferences
    locations = ["Cabot Library", "Dorm Room", "Lamont Library", "Smith Center", "Widener Library"]
    if request.method == "POST":
        error = ""
        # Assume that course is the course they enter into the form
        # Assume that size is the size preference they enter into the form
        # Assume that locationlist is the single location they enter into the form 
        course = request.form.get("course")
        # Check that course as submitted is an integer with six digits
        if not course.isdigit() or len(str(course))!=6:
            error = "Make sure you are submitting a six number course ID, not the course name!"
            return render_template("prefs.html", locations = locations, daysoftheweek = daysoftheweek, time_to_index = time_to_index, error = error)
        # Obtain email from the session id for the currently signed in user
        email = session["user_id"]
        size = request.form.get("size")
        locationlist = request.form.get("location")
        # Create a time dictionary relating day of the week with corresponding times they meet
        timeDict = {}
        # We looked at this resource: https://stackoverflow.com/questions/12502646/access-multiselect-form-field-in-flask
        # Find all the times the user submitted in their preferences form with the corresponding days they want to meet on at those times
        for x in daysoftheweek: 
            timeDict[x] = request.form.getlist(x)
            timestring = ""
            for y in timeDict[x]: 
                timestring += y +","
            timestring = timestring[0:len(timestring)-1]
            timeDict[x] = timestring
            table = db.execute("SELECT course FROM prefs WHERE email = ? AND course = ? AND day = ?", email, course, x)
            try:
                # If the entry exists in the table (the user has previously submitted a preference form for that course on that day); update the existing entry
                if len(table[0]['course']) > 0:
                    db.execute("UPDATE prefs SET size = ?, times = ?, locations = ? WHERE email = ? AND course = ? AND day = ?", size, timeDict[x], locationlist, email, course, x)
               # If the entry in the table is blank (the user has not previously submitted a preference form for that course on that day); create a new entry
                else:
                    db.execute("INSERT INTO prefs (email, course, size, times, locations, day) VALUES (?, ?, ?, ?, ?, ?)", email, course, size, timeDict[x], locationlist, x)
           # If not able to open the entry in the table (the user has not previously submitted a preference form for that course on that day); create a new entry
            except:
                db.execute("INSERT INTO prefs (email, course, size, times, locations, day) VALUES (?, ?, ?, ?, ?, ?)", email, course, size, timeDict[x], locationlist, x)
        # Format the prefs html, sending the list of locations, days of week, and times
        return render_template("prefs.html", locations = locations, daysoftheweek = daysoftheweek, time_to_index = time_to_index)

    else:
        # Format the prefs html, sending the list of locations, days of week, and times
        return render_template("prefs.html", locations=locations, daysoftheweek = daysoftheweek, time_to_index = time_to_index)

# Handles emailing the matched study groups 
def matchemail(people, locations, timeblock, day, uniqueCourse, matched):
    # We looked at this resource to count values: https://www.programiz.com/python-programming/methods/string/count
    # Create a dictionary whose keys are the locations and whose initial values are zero
    places = {
                "Cabot Library": 0, 
                "Dorm Room": 0, 
                "Lamont Library": 0, 
                "Smith Center": 0, 
                "Widener Library": 0
            }
    # Check how many times each location appears in the list "locations" that is passed in through grouper
    for key in places: 
        places[key] = locations.count(key)
    # Rename the places dictionary as locations
    locations = places 
    # People is a list of emails for the people matched in the group
    # Locations is a dictionary whose keys are the list of locations and values are how many people want that location 
    # UniqueCourse is an integer valiue
    # Matched will be a boolean telling whether the group of people are matched or unmatched
    # Day is a single day because we are only matching for one day for the group
    
    # Find how many people are in the group
    count = len(people)
    if not matched:
        timesdictSunday={}
        timesdictMonday={}
        timesdictTuesday={}
        timesdictWednesday = {}
        timesdictThursday = {}
        timesdictFriday = {}
        timesdictSaturday = {}
        # Create a list of dictionaries, where each dictionary corresponds to a different day of the week
        fulllistoftimes =[timesdictSunday,timesdictMonday, timesdictTuesday, timesdictWednesday, timesdictThursday, timesdictFriday, timesdictSaturday]
        daycount = 0
        for aday in daysoftheweek:
            # Indexes fulllistoftimes to temporarily assign timesdict to the corresponding dictionary in fulllistoftimes
            timesdict = fulllistoftimes[daycount]
            for person in people:
                # Find all the preferred times for all the people in this group on the specific day 
                timetable = db.execute("SELECT times FROM prefs WHERE email LIKE ? AND course = ? AND day = ?", person, uniqueCourse, aday)
                timelist = timetable['times'].split(",")
                # Count how many people in the group prefer each time on that day
                for entry in timelist:
                    if timesdict.has_key(entry):
                        timesdict[entry] = timesdict[entry] + 1
                    else:
                        timesdict[entry] = 1
            daycount = daycount + 1
       # Create custom timetext for unmatched people, to go through the dictionary and let them know how many people prefer each time each day
        timetext = " Of people who were unmatched, "
        for x in range(7):
            timesdict = fulllistoftimes[x]
            for entry in timesdict:
                if timesdict.has_key(entry):
                    timetext = timetext + timetext[entry] + " people prefer " + entry + " on " + daysoftheweek[x] + ". "
        # Create custom locationtext for unmatched people, to go through the dictionary of locations and let them know how many people prefer each location
        locationtext = " Of people who were unmatched: "
        for entry in locations:
            locationtext = locationtext + " "+ str(locations[entry]) + " people prefer " + entry + "."
        # Create list of firstnames to address in the email, pulling it using their emails
        names = ""
        for person in people:
            if names == "":
                names = db.execute("SELECT firstname from users WHERE email = ?", person)['firstname']
            else:
                names = names + ", " + db.execute("SELECT firstname from users WHERE email = ?", person)['firstname']

        msg = Message(
                    'An Update on Your Study Group:',
                    sender ='study.groupmatching@gmail.com',
                    recipients = people
                    )
                    # String formatting in python: https://realpython.com/python-string-formatting/
        
        # Create sample email to send to unmatched people, which is filled in with the appropriate names, course, timetext, and locationtext
        t = 'Hello, $name. Unfortunately, we were not able to find a perfect match for you for $course. Nevertheless, we are sending a list of preferred times and locations for other people in your class who need a group: '
        t = t.replace('$name', names)
        t = t.replace('$course', uniqueCourse)
        t = t + timetext
        t = t+ locationtext
        print(t)
        msg.body = t
        with app.app_context():
           mail.send(msg)
        return 'Sent'

    if matched:
        # Convert locations dictionary into a string for matched people of where people at that time in that course prefer to meet
        locationtext = " Of people who plan to meet at this time (whether in your group or not): \n"
        for entry in locations:
            locationtext = locationtext + " "+ entry + ": "+str(locations[entry]) + "\n"
        # Go through all the emails of the matched people and pull their first names using the users database
        names = ""
        for person in people:
            if names == "":
                table = db.execute("SELECT firstname from users WHERE email = ?", person)
                names=table[0]['firstname']
            else:
                table = db.execute("SELECT firstname from users WHERE email = ?", person)
                names = names + ", " + table[0]['firstname']

        msg = Message(
                    'You have been matched!',
                    sender ='study.groupmatching@gmail.com',
                    recipients = people
                    )
                    # String formatting in python: https://realpython.com/python-string-formatting/
        # Formatted email customized to the names of the people in the group, their course, the day they meet, the time they meet, and locations people prefer
        t = 'Hello, name. We wanted to let you know that you have been matched! Your group for course will meet on day at time.'
        t = t.replace('name', names)
        t = t.replace('course', uniqueCourse)
        t = t.replace('day', day)
        # Converts the list timeblock into a string timestring which goes from first index to last index separated by a dash (10:00 AM, 10:30 AM, 11:00 AM becomes 10:00 AM-11:00 AM)
        timestring = ""
        if len(timeblock) == 2 and timeblock[0] == timeblock[1]:
            timestring = timeblock[0]
        else:
            timestring = timeblock[0]+"-"+timeblock[len(timeblock)-1]
        t = t.replace("time", timestring)
        t = t + locationtext
        print(t)
        msg.body = t
        with app.app_context():
           mail.send(msg)
        return 'Sent'

# This is the match algorithm that matches people into study groups 
def match(): 
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

# Prrereq = the sorting has already been filtered by course 
# This handles finding the timeblocks where the most people can be matched into study groups 
def timematch(uniqueCourse, day): 
    # stackedTimelines stores how many people are available at each time represented by each index of 
    # stackedTimelines 
    # assume 
    # https://stackoverflow.com/questions/57594419/2d-array-in-python-changes-the-whole-row-when-i-only-want-to-change-1-itemis-th
    stackedTimelines = []
    for x in range(0,48):
            row = []
            for x in range(0,2):
                row.append(0)
            stackedTimelines.append(row)
   
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
            stackedTimelines[time_to_index[time]][0] += 1 #number of people
            stackedTimelines[time_to_index[time]][1]= time
        
    stackedTimelines = sorted(stackedTimelines, key=lambda x: x[0], reverse = True)
   
    # Now stackedtimelines has the number of people who want a specific course at each time block 
    # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
    #sortedStackedTimelines = sorted(stackedTimelines.items(), key=lambda x: x[1], reverse=True)
    # Now stackedTimelines is sorted according by popularity of time and stored as a dictionary in sortedStackedTimelines
    # https://realpython.com/iterate-through-dictionary-python/
    # stackedTimelinesKeys = stackedTimelines.keys()
    # stackedTimelinesValues = stackedTimelines.values()

    #https://www.kite.com/python/answers/how-to-sort-a-multidimensional-list-by-column-in-python
    key = 0 
    duplicates = []
    while key < len(stackedTimelines):
        max_value = stackedTimelines[key][0]
        if max_value == 0 or max_value == 1: 
            break
        # finds 30 minute blocks with max people 
        # https://www.programiz.com/python-programming/methods/list/index
        timeblock = []
        am_timeblock = []
        pm_timeblock = []
        max_time = stackedTimelines[key][1]
        peopledict = db.execute("SELECT email FROM prefs WHERE course = ? AND times LIKE ? AND day = ?;", uniqueCourse, "%"+max_time+"%", day)
        people = []
        for x in peopledict: 
            people.append(x["email"])
        # now we have the list of people who the most popular 30 minute block works with
        # we wil now look to before and after this 30 minute block to see if the same people are available for a longer
        # block of time 
        if max_time[len(max_time)-2] == "am":
            am_timeblock.append(max_time)
        else: 
            pm_timeblock.append(max_time)
        max_index = time_to_index[max_time]
        count = 0
        for right in range(max_index, len(stackedTimelines)):
            key2 = index_to_time[right]
            peopledict2 = db.execute("SELECT email FROM prefs WHERE course = ? AND times LIKE ? AND day = ?;", uniqueCourse, "%"+key2+"%", day)
            people2 = []
            for x in peopledict2: 
                people2.append(x["email"]) 
            #https://thispointer.com/python-check-if-a-list-contains-all-the-elements-of-another-list/#:~:text=Check%20if%20list1%20contains%20all%20elements%20of%20list2%20using%20all()&text=Python%20all()%20function%20checks,if%20element%20exists%20in%20list1.
            contained =  all(elem in people2  for elem in people)
            if not contained:
                break
            else: 
                 count += 1
                 if key2[len(key2)-2] == "am":
                    am_timeblock.append(key2)
                 else: 
                    pm_timeblock.append(key2)
        am_timeblock.sort()
        pm_timeblock.sort()
        timeblock = am_timeblock+pm_timeblock
        for person in people:
            if person in duplicates:
                break
            if not person in duplicates:
                grouper(uniqueCourse, timeblock, people, day)
                for r in people: 
                    duplicates.append(r)
        key += 1
        key += count
    

# Prereq = the sorting has already been filtered by course and time 
# Grouping algorithm for people for a particular time interval by group size 
def grouper(uniqueCourse, timeblock, emails, day):
    timestring = ""
    locationstring = ""
    for i in range(1, len(timeblock)):
        time = timeblock[i]
        timestring += time + ","
    timestring = timestring[0: len(timestring)-1]
    course_entries = db.execute("SELECT * FROM prefs WHERE course = ? AND times LIKE ? AND day = ?", uniqueCourse, "%"+timestring+"%", day)
    course_locations = db.execute("SELECT locations FROM prefs WHERE course = ? AND times LIKE ? AND day = ?", uniqueCourse, "%"+timestring+"%", day)
    locationstring = ""
    for x in course_locations: 
        locationstring+=x["locations"]
   
    number_of_people = len(course_entries)
    # If there are less than 3 people with the matching time, they are automatically put into a small group together
    if number_of_people <= 3:
        matchemail(emails, locationstring, timeblock, day, uniqueCourse, True)  
    # If there are 4-6 people with the same matching time, then if there are more people who prefer small group than large, we make two small groups
    elif number_of_people <=6 and number_of_people >=4:
       large = sizeCount(course_entries, "l")
       medium = sizeCount(course_entries, "m")
       small = number_of_people - large - medium  
       if small > (medium + large): 
           if number_of_people == 4: 
               matchemail(emails[0:2], locationstring, timeblock, day, uniqueCourse, True)
               matchemail(emails[2:4], locationstring, timeblock, day, uniqueCourse, True)
           elif number_of_people == 5: 
               matchemail(emails[0:2], locationstring, timeblock, day, uniqueCourse, True)
               matchemail(emails[2:5], locationstring, timeblock, day, uniqueCourse, True)
           else: 
               matchemail(emails[0:3], locationstring, timeblock, day, uniqueCourse, True)
               matchemail(emails[3:6], locationstring, timeblock, day, uniqueCourse, True)
       else:
           # If the amount of people who prefer small group is not the majority, everyone is placed together as a medium group
           matchemail(emails, locationstring, timeblock, day, uniqueCourse, True) 
    else: # 7+ people who are in the same timeblock
       large = sizeCount(course_entries, "l")
       medium = sizeCount(course_entries, "m")
       small = number_of_people - large - medium
       large_people_dict = db.execute("SELECT email FROM prefs WHERE course = ? AND timeblock LIKE ? AND day = ? AND size = ?", uniqueCourse, "%"+timeblock+"%", day, "l")
       large_people = []
       # Creates a list of the emails of people in the same timeblock who prefer large groups
       for t in large_people_dict: 
           large_people.append(large_people_dict["email"])
       medium_people_dict = db.execute("SELECT email FROM prefs WHERE course = ? AND timeblock LIKE ? AND day = ? AND size = ?", uniqueCourse, "%"+timeblock+"%", day, "m")
       medium_people = []
       # Creates a list of the emails of people in the same timeblock who prefer medium groups
       for t in medium_people_dict: 
           medium_people.append(medium_people_dict["email"])
       small_people_dict = db.execute("SELECT email FROM prefs WHERE course = ? AND timeblock LIKE ? AND day = ? AND size = ?", uniqueCourse, "%"+timeblock+"%", day, "s")
       small_people = []
       # Creates a list of the emails of people in the same timeblock who prefer large groups
       for t in small_people_dict:
           small_people.append(small_people_dict["email"])
       if small == 1:
           # If there is only one person who prefers small, that isn't enough to form a small group so we move them to preferring medium
            medium = medium + small
            small = 0
            medium_people.append(small_people.pop())
       s = small
       # We want to ensure that there are at least 4 people in the medium group, so we group as many people who prefer small into small group as possible, while ensuring at least four people are in the medium group
       if number_of_people - s < 4:
            s = number_of_people - 4
       smallbutnots = small - s
       medium = medium + smallbutnots
       for x in range(smallbutnots):
           medium_people.append(small_people.pop())
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