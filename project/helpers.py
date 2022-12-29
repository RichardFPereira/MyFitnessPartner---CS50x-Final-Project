from flask import redirect, render_template, request, session
from functools import wraps
from cs50 import SQL

def muscles():
    muscle = ["None","Biceps", "Back", "Calves", "Cardio", "Chest", "Core", "Legs", "Rest", "Trapezius", "Triceps", "Shoulders"]
    return muscle

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def todayExercises(todayTrainning, userId):
    workoutTable = SQL("sqlite:///workout.db")
    exercises = {}
    for i in range(len(todayTrainning)):
        todayTrainning[i] = todayTrainning[i].lower()
        if(todayTrainning[i] != "rest"):
            muscle = workoutTable.execute("SELECT * FROM ? WHERE user_id = ?", (todayTrainning[i]+"Workout"), userId)
            for j in range(len(muscle)):
                addValue(exercises, todayTrainning[i], muscle[j][todayTrainning[i]+"exercises"])
        else:
            exercises = todayTrainning[i]
            return exercises
    return exercises

def addValue(dict_obj, key, value):
    if key not in dict_obj:
        dict_obj[key] = value
    elif isinstance(dict_obj[key], list):
        dict_obj[key].append(value)
    else:
        dict_obj[key] = [dict_obj[key], value]