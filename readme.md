Video: https://youtu.be/OM6oV4jEoAI
pip install the following packages: 
The Front-End:
Use flask run to generate the study.group website.

You will be taken to the main page of the study.group website.

If you have already registered for an account, click “login” at the top of the page to take you to the login page of the website.

If you have not already registered, you should register to make an account. Click “register” at the top of the page to take you to the registration form. Make sure that you fill out all the fields required for registration (first name, last name, email, make up a password, confirm password). If fields are not filled out when the submit button is clicked or the password confirmation does not match the password you chose, you will remain on the register page and an error message will appear at the bottom of the form telling you what went wrong.

If you correctly register for an account, you should be automatically taken to the login page of the site and you will see a “WELCOME!” message displayed on the left-hand side of the page.

After registering, you should be able to login with the account you just created, using your email and the password you signed up with.

After logging in, the menu at the top of the page will change. You should now be able to see “preferences”, “courses”, and “logout” at the top of the page, as well as the home page. 

Click “preferences”--you should see the form to submit group preferences:
	In this form, you will be asked to provide the course you wish to find a study group for.
The course should be entered not as its name (i.e. CS50) but instead its ID which can be found in my.harvard.edu (i.e. 152514).
Enter all the days and times you are available to meet (note that the algorithm may put you in multiple groups; one for each day). There should be seven different select menus, each labeled with a day of the week to input the times you are available to meet at that day of the week. To select times in the select menu, click on the time you are available. To select multiple times all in a block, hold shift and click. To select multiple times not in a block, hold command and click. If you are not available at any time during a day of the week, do not select any times.
Enter your preferred location and your preferred group size (the preferred location won’t affect which group you end up in, but its results will be sent to all groups meeting at that time to give students a better idea of where they might want to meet) by clicking on the select menu and selecting which location (Cabot Library, Dorm Room, Lamont Library, Smith Center, or Widener Library) and which group size (Small 2-3 people, Medium 4-6 people, or Large 7 or more people) you prefer.
After submitting the form, you can either submit the form again for a different class (if you want to find a study group for another class) or submit the form again for the same class (which will update your preferences in the database).

You can also click on the courses tab to see the current courses you have filled out preferences for. You should be able to see resource links that other students have provided for that course. If you have any suggestions for resources for that course, you can submit a url to that resource as well as the resource’s title, and we will display the link as the title of the resource for other students in that course looking for resources! Make sure to submit the url for your resourcelink including https:// at the beginning, otherwise there will be errors!

If you’re all done using the site, you can click log out! Thanks for using our website!

The Back-End:
In an ideal world, the matching algorithm would be called periodically whenever study groups needed to be made (likely once per week or once per night depending on how much advance notice we wanted to give students). Unfortunately, for the sake of demonstration, this is not really feasible. As a result, we have called the match() function directly in app.py. Thus, when you run flask run to generate the website, you will also be running the matching algorithm.

Since (unless your email happened to already be in the database as someone who was going to be matched) you likely won’t actually receive the matching email, we have printed to the console what the email would look like for each group that got matched.

Thus, you should be able to see all the groups the matching algorithm formed as well as their customized emails that our program sends from the study.group email.

If you put enough test data into the front-end to guarantee a match and run flask, you may be able to see the email for yourself in your inbox!
