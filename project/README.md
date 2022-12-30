# MY FITNESS PARTNER

### Video Demo: <https://www.youtube.com/watch?v=0-JElocpAsk>

### Description
Hello guys! This is my final project for CS50x course.
I've created a online workout web page where you can login and create your own workout trainning plan.

I've used Python with the Flask framework in the backend and HTML, CSS, JavaScript and Bootstrap in the frontend.
For the database I've used SQLite to handle user login, password and data about training schedules, muscles and exercises.

## app.py

This is our main code for the data backend and it handles the routs for our pages.

    I've imported some libraries to help in my development.
    - The SQL function from cs50 library allows me to handle the data in my databases.
    - From the werkzeug.security library I've imported the check_password_hash and generate_password_hash
    - I've also created a new library to help me with some functions that will be discussed later

    * The register route ('/register' - 'register.html'):
        - For the first access, the user need to be register. By clicking on the navbar button 'Register', the user will be redirected to the register page and will be asked to write their username, password and confirmation password.

        - If the username is already in the users data base (users.db), the user will receive an error message saying that username is already taken.

        - If the password and the confirmation password doesn't match, the user will receive an error message saying that the both pass must be equal.

        - If the username is empty, it will give the user an error saying the user should provide an username.

        - If all requirements are right the username will be capitalized and stored with the password inside users table and the user will be logged and redirected to the main page ('/' - index.html).


    * The login route ('/login' - login.html):
        - This route will allow the user to login in their account.

        - The first action this route will do is to clear all user session.

        - If the method used to reach this route is GET, it will promp to the user a login page asking for login and password.

        - After the user provide the loggin information, the route will be reach via POST and will ensure if the user wrote a proper username and password for a registered user. If everything is right, the user will be logged and will be redirected to the main page ('/' - index.html).


    * The main page route ('/' - 'index.html'):
        - To access this page the user need to be logged and the login_required function imported from helpers.py insure if the user is logged. If not, will be redirecte to the login page.

        - If the user is logged, this route will get the user name to greet the user, the user id to know who is logged and will verify if the logged user already have any workout exercise in user workout TABLE.

        - If the workout table is empty it will show the user a message asking to create the first training.

        - In case of the user already have a workout plan, it will display to the user the workout for the week day of today.

    * The custom route ('/custom' - custom.html):
        - This rout is responsible to create the week schedule for the user. It can be reach from the main page option when the user doesn't have any workout plan or anytime for a logged user by clicking on the navbar button Edit Workout.

        - If the route is reach by a GET method, the custom.html template will be show to the user. This template will allow the user to select the muscles for each day of the week using a dropdown menu with twelve options: "None","Biceps", "Back", "Calves", "Cardio", "Chest", "Core", "Legs", "Rest", "Trapezius", "Triceps", "Shoulders".

        - After the user selects the schedule and clicks to create the plan, the route will be reached via POST method. Then the next steps will happen:

            - An empty array will be declared for each day of a week and a variable to store the logged user id will be declared as well.

            - After get the logged user, it will seek for a workout training for that user, if the user already have a workout plan, the table will be clear to create a new one. If the user doesn't have any plan, then a new one will be created as well.

            - All the muscles selected by the user before will be saved inside the array for each muscle and than, inside the exercises table (exercises.db). If the user left any choice as 'Rest' or 'None' it will be ignored by the progam and will not be saved in the database.

            - After that, the user will be redirected to the '/exercises' route (exercises.html) to select the exercises for each muscle.

    * The exercises route ('/exercises' - exercises.html):
        - This route will show the user a button for each muscle and when clicked they will show four dropdown menus with some exercises for that muscle. The user need to select the exercises they want to do and save it.

        - When reach by POST method (after the user select the exercises and summited), this route will fill lists for each muscle with the selected muscles and avoid "NONE" options or exercises already selected.

        - If the user already have a list of exercises for the selected muscle, it will be cleared and the new one will be saved. If this is the first list of exercises for that muscles, it will be saved as well.

        - After the list is save inside the workout table (workout.db), the user is redirected to the main page showing the training list for actual day of week.


## helpers.py

    This file contains four functions to help the main program (app.py) work property.

    * muscle():
        A list of the muscles included inside the program and return that list. Used just to better organize the code.

    * login_required():
        This function ensure if the user is logged or not.

    * todayExercises():
        This function receives a list of training and the user id. It will return the muscles for the actual day of week.

    * addValue():
        This function receives data from todayExercises to create a object list where each key can have more than one value.

## /static

    * styles.css:
        This file have css code to change the style of few html tags and objects.

    * script.js:
        - The hideShowExercises() function is responsible to hide/show the exercises list inside the exercises.html table by clicking on the muscle button.

        - The checkTrainning() function is responsible to change the property of the text when the checkbox is clicked inside the index.html file.

## /templates

    * base.html:
        - This is the layout html tamplate used in all pages of this web app.
        - It creates the navbar at the top and a footer with my GitHub hyperlink.
        - It also import bootstrap and script from bootstrap website.
        - When there is no user logged, it will show a navbar with MyFitnessPartner button (redirect to homepage), Log In (redirect to login page) button and Register (redirect to register page) button. If there is a user logged, the navbar will change Log In and Register for Edit Workout (redirect to custom page), Edit Exercises (redirect to exercises page) and Log Out (log hte user out and redirect to login page) buttons.

    * custom.html:
        - Import base.html layout.
        - Show the table with days of week and four rows of data for each day of week.
        - Each row has twelve options of choice inside a dropdown menu: "None","Biceps", "Back", "Calves", "Cardio", "Chest", "Core", "Legs", "Rest", "Trapezius", "Triceps", "Shoulders"
        - Each table data has their own id to pass the value to the app.py file to handle data.
