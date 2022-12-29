from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import muscles, login_required, todayExercises

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Uses CS50 library to handle database
exercisesTable = SQL("sqlite:///exercises.db")
userTable =  SQL("sqlite:///users.db")
weekScheduleTable = SQL("sqlite:///week_schedule.db")
workoutTable = SQL("sqlite:///workout.db")

@app.route('/')
@login_required
def index():
    todayTrainning = []
    weekDay = datetime.now()
    userId = session.get("user_id")
    username = userTable.execute("SELECT username FROM users WHERE user_id = ?", userId)
    username = username[0]["username"]
    week = weekScheduleTable.execute("SELECT * FROM week_schedule WHERE user_id = ?", userId)

    biceps = workoutTable.execute("SELECT * FROM bicepsWorkout WHERE user_id = ?", userId)
    back = workoutTable.execute("SELECT * FROM bicepsWorkout WHERE user_id = ?", userId)
    calves = workoutTable.execute("SELECT * FROM calvesWorkout WHERE user_id = ?", userId)
    cardio = workoutTable.execute("SELECT * FROM cardioWorkout WHERE user_id = ?", userId)
    chest = workoutTable.execute("SELECT * FROM chestWorkout WHERE user_id = ?", userId)
    core = workoutTable.execute("SELECT * FROM coreWorkout WHERE user_id = ?", userId)
    legs = workoutTable.execute("SELECT * FROM legsWorkout WHERE user_id = ?", userId)
    trapezius = workoutTable.execute("SELECT * FROM trapeziusWorkout WHERE user_id = ?", userId)
    triceps = workoutTable.execute("SELECT * FROM tricepsWorkout WHERE user_id = ?", userId)

    workout = True
    if ((len(biceps) != 0) or (len(back) != 0) or (len(calves) != 0) or (len(cardio) != 0) or (len(chest) != 0) or (len(core) != 0) or (len(legs) != 0) or (len(trapezius) != 0) or (len(triceps) != 0)):
        exercises = False
        workout = False

    if (len(week) == 0 or workout == True):
        exercises = False
        hasTrain = False
    else:
        hasTrain = True
        weekDay = weekDay.strftime('%A').lower()
        for i in range(4):
            if (week[i][weekDay] != "None"):
                todayTrainning.append(week[i][weekDay])
        weekDay = weekDay.capitalize()
        exercises = todayExercises(todayTrainning, userId)

    return render_template('index.html', hasTrain = hasTrain, username = username, todayTrainning = todayTrainning, weekDay = weekDay, muscles = len(todayTrainning), exercises = exercises, biceps = biceps)

@app.route('/login', methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('error.html', error="MUST PROVIDE USERNAME!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('error.html', error="MUST PROVIDE PASSWORD!")

        # Query database for username
        username = request.form.get("username")
        username = username.capitalize()
        password = request.form.get("password")

        rows = userTable.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return render_template('error.html', error="INVALID USERNAME OR PASSWORD!")

        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    # Forget any user_id
    session.clear()

    # User reached route via post (subimitting register form)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template('error.html', error="MUST PROVIDE USERNAME!")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template('error.html', error="MUST PROVIDE PASSWORD!")

        # Ensure password was submitted
        elif not request.form.get("confirmPass"):
            return render_template('error.html', error="MUST PROVIDE CONFIRMATION PASSWORD!")

        username = request.form.get("username")
        username = username.capitalize()
        password = request.form.get("password")
        confirmPass = request.form.get("confirmPass")

        # Verify is both passwords are equal
        if password != confirmPass:
            return render_template('error.html', error="PASSWORD AND CONFIRMATION PASSWORD MUST BE EQUAL!")

        # Query database for username
        rows = userTable.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username is available
        if len(rows) != 0:
            return render_template('error.html', error="USERNAME IS ALREADY IN USE!")

        # If the username is available, insert new data into the users table
        userTable.execute("INSERT INTO users (username, hash) VALUES (?,?)", username, generate_password_hash(password))

        # Remember which user has logged in
        users = userTable.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = users[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")

@app.route('/custom', methods=["GET", "POST"])
@login_required
def custom():
    if request.method == "POST":
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        saturday = []
        sunday = []
        userId = session.get("user_id")

        loggedUser = weekScheduleTable.execute("SELECT * FROM week_schedule WHERE user_id = ?", userId)
        if (len(loggedUser) != 0):
            weekScheduleTable.execute("DELETE FROM week_schedule WHERE user_id = ?", userId)

        for i in range(1,5):
            monday.append(request.form.get("monday"+str(i)))
            tuesday.append(request.form.get("tuesday"+str(i)))
            wednesday.append(request.form.get("wednesday"+str(i)))
            thursday.append(request.form.get("thursday"+str(i)))
            friday.append(request.form.get("friday"+str(i)))
            saturday.append(request.form.get("saturday"+str(i)))
            sunday.append(request.form.get("sunday"+str(i)))

        for i in range(4):
            weekScheduleTable.execute("INSERT INTO week_schedule (user_id, monday, tuesday, wednesday, thursday, friday, saturday, sunday) VALUES (?,?,?,?,?,?,?,?)", userId, monday[i], tuesday[i], wednesday[i], thursday[i], friday[i], saturday[i], sunday[i])

        biceps = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Biceps'")
        backs = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Back'")
        calves = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Calves'")
        chests = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Chest'")
        cores = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Core'")
        legs = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Legs'")
        trapezius = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Trapezius'")
        triceps = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Triceps'")
        muscle = muscles()

        return render_template('exercises.html', muscle=muscle, biceps=biceps, backs=backs, calves=calves, chests=chests, cores=cores, legs=legs, trapezius=trapezius, triceps=triceps)
    else:
        return render_template('custom.html')

@app.route('/exercises', methods=["GET", "POST"])
@login_required
def exercises():
    biceps = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Biceps'")
    backs = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Back'")
    calves = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Calves'")
    chests = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Chest'")
    cores = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Core'")
    legs = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Legs'")
    trapezius = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Trapezius'")
    triceps = exercisesTable.execute("SELECT * FROM exercises WHERE muscle = 'Triceps'")
    muscle = muscles()

    if request.method == "POST":

        bicepsExercises = []
        bicepsSets = []
        bicepsReps = []
        backExercises = []
        calvesExercises = []
        cardioExercises = []
        chestExercises = []
        coreExercises = []
        legsExercises = []
        trapeziusExercises = []
        tricepsExercises = []
        userId = session.get("user_id")

        #Fill muscles lists with exercises selected by the user
        #Avoiding "NONE" values and exercises already on the list
        for i in range(1,5):
            if ((request.form.get("Biceps"+str(i))) != "NONE" and (request.form.get("Biceps"+str(i))) not in bicepsExercises):
                bicepsExercises.append(request.form.get("Biceps"+str(i)))
                bicepsSets.append(request.form.get("sets"+"Biceps"+str(i)))
                bicepsReps.append(request.form.get("reps"+"Biceps"+str(i)))

            if ((request.form.get("Back"+str(i))) != "NONE" and (request.form.get("Back"+str(i))) not in backExercises):
                backExercises.append(request.form.get("Back"+str(i)))

            if ((request.form.get("Calves"+str(i))) != "NONE" and (request.form.get("Calves"+str(i))) not in calvesExercises):
                calvesExercises.append(request.form.get("Calves"+str(i)))

            if (request.form.get("Cardio"+str(i)) != "" and (request.form.get("Cardio"+str(i)) not in cardioExercises)):
                cardioExercises.append(request.form.get("Cardio"+str(i)))

            if ((request.form.get("Chest"+str(i))) != "NONE" and (request.form.get("Chest"+str(i))) not in chestExercises):
                chestExercises.append(request.form.get("Chest"+str(i)))

            if ((request.form.get("Core"+str(i))) != "NONE" and (request.form.get("Core"+str(i))) not in coreExercises):
                coreExercises.append(request.form.get("Core"+str(i)))

            if ((request.form.get("Legs"+str(i))) != "NONE" and (request.form.get("Legs"+str(i))) not in legsExercises):
                legsExercises.append(request.form.get("Legs"+str(i)))

            if ((request.form.get("Trapezius"+str(i))) != "NONE" and (request.form.get("Trapezius"+str(i))) not in trapeziusExercises):
                trapeziusExercises.append(request.form.get("Trapezius"+str(i)))

            if ((request.form.get("Triceps"+str(i))) != "NONE" and (request.form.get("Triceps"+str(i))) not in tricepsExercises):
                tricepsExercises.append(request.form.get("Triceps"+str(i)))

        # The logic used for biceps is the same for other muscles
        # Select bicepsWorkout table for the logged user
        bicepsWorkout = workoutTable.execute("SELECT * FROM bicepsWorkout WHERE user_id = ?", userId)
        # Verify if the logged user already have a biceps workout
        # If not, insert selected exercises inside biceps table for that user
        if (len(bicepsWorkout) == 0):
            # Loop through the list of selected biceps exercises
            for i in range(len(bicepsExercises)):
                if (bicepsExercises[i] != ""):
                    workoutTable.execute("INSERT INTO bicepsWorkout (user_id, bicepsExercises, sets, reps) VALUES (?,?,?,?)", userId, bicepsExercises[i], bicepsSets[i], bicepsReps[i])
        # If user already have a biceps workout delete that data and
        # Create a new table with selected exercises
        else:
            workoutTable.execute("DELETE FROM bicepsWorkout WHERE user_id = ?", userId)
            for i in range(len(bicepsExercises)):
                if (bicepsExercises[i] != ""):
                    workoutTable.execute("INSERT INTO bicepsWorkout (user_id, bicepsExercises, sets, reps) VALUES (?,?,?,?)", userId, bicepsExercises[i], bicepsSets[i], bicepsReps[i])

        backWorkout = workoutTable.execute("SELECT * FROM backWorkout WHERE user_id = ?", userId)
        if (len(backWorkout) == 0):
            for i in range(len(backExercises)):
                if (backExercises[i] != ""):
                    workoutTable.execute("INSERT INTO backWorkout (user_id, backExercises) VALUES (?,?)", userId, backExercises[i])
        else:
            workoutTable.execute("DELETE FROM backWorkout WHERE user_id = ?", userId)
            for i in range(len(backExercises)):
                if (backExercises[i] != ""):
                    workoutTable.execute("INSERT INTO backWorkout (user_id, backExercises) VALUES (?,?)", userId, backExercises[i])

        calvesWorkout = workoutTable.execute("SELECT * FROM calvesWorkout WHERE user_id = ?", userId)
        if (len(calvesWorkout) == 0):
            for i in range(len(calvesExercises)):
                if (calvesExercises[i] != ""):
                    workoutTable.execute("INSERT INTO calvesWorkout (user_id, calvesExercises) VALUES (?,?)", userId, calvesExercises[i])
        else:
            workoutTable.execute("DELETE FROM calvesWorkout WHERE user_id = ?", userId)
            for i in range(len(calvesExercises)):
                if (calvesExercises[i] != ""):
                    workoutTable.execute("INSERT INTO calvesWorkout (user_id, calvesExercises) VALUES (?,?)", userId, calvesExercises[i])

        cardioWorkout = workoutTable.execute("SELECT * FROM cardioWorkout WHERE user_id = ?", userId)
        if (len(cardioWorkout) == 0):
            for i in range(len(cardioExercises)):
                if (cardioExercises[i] != ""):
                    workoutTable.execute("INSERT INTO cardioWorkout (user_id, cardioExercises) VALUES (?,?)", userId, cardioExercises[i])
        else:
            workoutTable.execute("DELETE FROM cardioWorkout WHERE user_id = ?", userId)
            for i in range(len(cardioExercises)):
                if (cardioExercises[i] != ""):
                    workoutTable.execute("INSERT INTO cardioWorkout (user_id, cardioExercises) VALUES (?,?)", userId, cardioExercises[i])

        chestWorkout = workoutTable.execute("SELECT * FROM chestWorkout WHERE user_id = ?", userId)
        if (len(chestWorkout) == 0):
            for i in range(len(chestExercises)):
                if (chestExercises[i] != ""):
                    workoutTable.execute("INSERT INTO chestWorkout (user_id, chestExercises) VALUES (?,?)", userId, chestExercises[i])
        else:
            workoutTable.execute("DELETE FROM chestWorkout WHERE user_id = ?", userId)
            for i in range(len(chestExercises)):
                if (chestExercises[i] != ""):
                    workoutTable.execute("INSERT INTO chestWorkout (user_id, chestExercises) VALUES (?,?)", userId, chestExercises[i])

        coreWorkout = workoutTable.execute("SELECT * FROM coreWorkout WHERE user_id = ?", userId)
        if (len(coreWorkout) == 0):
            for i in range(len(coreExercises)):
                if (coreExercises[i] != ""):
                    workoutTable.execute("INSERT INTO coreWorkout (user_id, coreExercises) VALUES (?,?)", userId, coreExercises[i])
        else:
            workoutTable.execute("DELETE FROM coreWorkout WHERE user_id = ?", userId)
            for i in range(len(coreExercises)):
                if (coreExercises[i] != ""):
                    workoutTable.execute("INSERT INTO coreWorkout (user_id, coreExercises) VALUES (?,?)", userId, coreExercises[i])

        legsWorkout = workoutTable.execute("SELECT * FROM legsWorkout WHERE user_id = ?", userId)
        if (len(legsWorkout) == 0):
            for i in range(len(legsExercises)):
                if (legsExercises[i] != ""):
                    workoutTable.execute("INSERT INTO legsWorkout (user_id, legsExercises) VALUES (?,?)", userId, legsExercises[i])
        else:
            workoutTable.execute("DELETE FROM legsWorkout WHERE user_id = ?", userId)
            for i in range(len(legsExercises)):
                if (legsExercises[i] != ""):
                    workoutTable.execute("INSERT INTO legsWorkout (user_id, legsExercises) VALUES (?,?)", userId, legsExercises[i])

        trapeziusWorkout = workoutTable.execute("SELECT * FROM trapeziusWorkout WHERE user_id = ?", userId)
        if (len(trapeziusWorkout) == 0):
            for i in range(len(trapeziusExercises)):
                if (trapeziusExercises[i] != ""):
                    workoutTable.execute("INSERT INTO trapeziusWorkout (user_id, trapeziusExercises) VALUES (?,?)", userId, trapeziusExercises[i])
        else:
            workoutTable.execute("DELETE FROM trapeziusWorkout WHERE user_id = ?", userId)
            for i in range(len(trapeziusExercises)):
                if (trapeziusExercises[i] != ""):
                    workoutTable.execute("INSERT INTO trapeziusWorkout (user_id, trapeziusExercises) VALUES (?,?)", userId, trapeziusExercises[i])

        tricepsWorkout = workoutTable.execute("SELECT * FROM tricepsWorkout WHERE user_id = ?", userId)
        if (len(tricepsWorkout) == 0):
            for i in range(len(tricepsExercises)):
                if (tricepsExercises[i] != ""):
                    workoutTable.execute("INSERT INTO tricepsWorkout (user_id, tricepsExercises) VALUES (?,?)", userId, tricepsExercises[i])
        else:
            workoutTable.execute("DELETE FROM tricepsWorkout WHERE user_id = ?", userId)
            for i in range(len(tricepsExercises)):
                if (tricepsExercises[i] != ""):
                    workoutTable.execute("INSERT INTO tricepsWorkout (user_id, tricepsExercises) VALUES (?,?)", userId, tricepsExercises[i])
        return redirect('/')
    else:
        return render_template('exercises.html', muscle=muscle, biceps=biceps, backs=backs, calves=calves, chests=chests, cores=cores, legs=legs, trapezius=trapezius, triceps=triceps)

@app.route('/clear_tables', methods=["GET", "POST"])
def clearTables():
    if request.method == "POST":
        userId = session.get("user_id")
        if request.form.get("clearUserTable") == "user":
            userTable.execute("DELETE FROM users")
            return redirect('/register')
        elif request.form.get("clearWeekSchedule") == "week":
            weekScheduleTable.execute("DELETE FROM week_schedule")
            return redirect('/')
        elif request.form.get("clearWorkoutTable") == "workout":
            workoutTable.execute("DELETE FROM cardioWorkout")
            workoutTable.execute("DELETE FROM backWorkout")
            workoutTable.execute("DELETE FROM bicepsWorkout")
            workoutTable.execute("DELETE FROM calvesWorkout")
            workoutTable.execute("DELETE FROM chestWorkout")
            workoutTable.execute("DELETE FROM coreWorkout")
            workoutTable.execute("DELETE FROM legsWorkout")
            workoutTable.execute("DELETE FROM trapeziusWorkout")
            workoutTable.execute("DELETE FROM tricepsWorkout")
            return redirect('/exercises')
    else:
        return render_template('clear_tables.html')