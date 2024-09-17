import os

import sqlite3
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

# Configure application
app = Flask(__name__)

# Configure the session to use the filesystem (instead of signed cookies)
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = "your_secret_key"

# Initialize the session
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# TODO:
# HARDCODED VARIABLES THAT SHOULD BE USER INPUT
user_id = 2

notes_sharps = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
notes_flats = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
strings = ['E', 'A', 'D', 'G', 'B', 'E']
# Temporary hard-coded e minor scale
e_minor_scale = ["E", "F#", "G", "A", "B", "C", "D"]

# Hard Coded Scales
# Using a sub-list to include both sharps and flats
# CONVERTING TO DICTIONARY
scales = {
    "c": ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    "g": ['G', 'A', 'B', 'C', 'D', 'E', ['F#', 'Gb']],
    "d": ['D', 'E', ['F#', 'Gb'], 'G', 'A', 'B', ['C#', 'Db']],
    "a": ['A', 'B', ['C#', 'Db'], 'D', 'E', ['F#', 'Gb'], ['G#', 'Ab']],
    "e": ['E', ['F#', 'Gb'], ['G#', 'Ab'], 'A', 'B', ['C#', 'Db'], ['D#', 'Eb']],
    "b": ['B', ['C#', 'Db'], ['D#', 'Db'], 'E', ['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb']],
    "gb": [['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb'], 'B', ['C#', 'Db'], ['D#', 'Eb'], 'F'],
    "db": [['C#', 'Db'], ['D#', 'Eb'], 'F', ['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb'], 'C'],
    "ab": [['G#', 'Ab'], ['A#', 'Bb'], 'C', ['C#', 'Db'], ['D#', 'Eb'], 'F', 'G'],
    "eb": [['D#', 'Eb'], 'F', 'G', ['G#', 'Ab'], ['A#', 'Bb'], 'C', 'D'],
    "bb": [['A#', 'Bb'], 'C', 'D', ['D#', 'Eb'], 'F', 'G', 'A'],
    "f": ['F', 'G', 'A', ['A#', 'Bb'], 'C', 'D', 'E']
}

# OLD HARDCODED SCALES
# c_major = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
# g_major = ['G', 'A', 'B', 'C', 'D', 'E', ['F#', 'Gb']]
# d_major = ['D', 'E', ['F#', 'Gb'], 'G', 'A', 'B', ['C#', 'Db']]
# a_major = ['A', 'B', ['C#', 'Db'], 'D', 'E', ['F#', 'Gb'], ['G#', 'Ab']]
# e_major = ['E', ['F#', 'Gb'], ['G#', 'Ab'], 'A', 'B', ['C#', 'Db'], ['D#', 'Eb']]
# b_major = ['B', ['C#', 'Db'], ['D#', 'Db'], 'E', ['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb']]
# gb_major = [['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb'], 'B', ['C#', 'Db'], ['D#', 'Eb'], 'F']
# db_major = [['C#', 'Db'], ['D#', 'Eb'], 'F', ['F#', 'Gb'], ['G#', 'Ab'], ['A#', 'Bb'], 'C']
# ab_major = [['G#', 'Ab'], ['A#', 'Bb'], 'C', ['C#', 'Db'], ['D#', 'Eb'], 'F', 'G']
# eb_major = [['D#', 'Eb'], 'F', 'G', ['G#', 'Ab'], ['A#', 'Bb'], 'C', 'D']
# bb_major = [['A#', 'Bb'], 'C', 'D', ['D#', 'Eb'], 'F', 'G', 'A']
# f_major = ['F', 'G', 'A', ['A#', 'Bb'], 'C', 'D', 'E']

# TODO:
# QUESTION: Is this still necessary?
# Types: list, char, bool
def generate_scale(scale, mode, pentatonic, sharps_or_flats):

    # temporary return
    return False

def generate_fretboard(string_count, fret_count, sharps_or_flats):
    # used to be universal list
    fretboard = []

    # Determine if using sharps or flats
    if sharps_or_flats == 'sharps':
        print("USING SHARPS")
        notes = notes_sharps
    elif sharps_or_flats == 'flats':
        print("USING FLATS")
        notes = notes_flats
    else:
        print("USING DEFAULT (SHARPS)")
        notes = notes_sharps

    print(f"STRING_COUNT: {string_count}")
    print(f"FRET_COUNT: {fret_count}")

    if not string_count or not fret_count:
        print("Must select option from both fields.")
        return redirect("parameters.html")

    # Clear the fretboard list at the start of the request
    fretboard.clear()

    for i in range(string_count):
        current_string = strings[i]
        string_frets = [current_string]  # Start with the open string note

        start_index = notes.index(current_string)

        for fret_index in range(1, fret_count + 1):
            note_index = (start_index + fret_index) % len(notes)
            string_frets.append(notes[note_index])

        print(f"CURRENT_STRING: {current_string}")
        print(f"STRING_FRETS: {string_frets}")

        fretboard.append(string_frets)

        # temp print (not permanent)
        print()
        for string in fretboard:
            print(string)
        print()

    # returning completed fretboard
    return fretboard

# fretboard (list of lists), notes (list of chars)
def render(fretboard, notes, sharps_or_flats):
    # Copy notes into new, local list to avoid manipulating glabal list
    local_notes = notes[:]

    # generate fretboard but just with desired notes (perhaps based on scale)

    for n, note in enumerate(local_notes):
        if type(local_notes[n]) is list:
            # Checking to see if the current note is a sharp/flat sub-list
            # Checking to see if sharps or flats are being used
            if (sharps_or_flats == "sharps"):
                # For the sub-list, index 0 = sharps and index 1 = flats
                # Setting the note at the index to one of the two notes in the sub-list given whether it is sharp or flat
                local_notes[n] = note[0]
            elif (sharps_or_flats == "flats"):
                local_notes[n] = note[1]
            else:
                print("ERROR: Trouble accessing sharps or flats sub-array in given scale array")
                # Setting 'x' as fret note to let user know that something is wrong

    # Remove notes on fretboard that are not in notes list specified by user
    for i, guitar_string in enumerate(fretboard):
        for j, fret_note in enumerate(guitar_string):
            if fret_note not in local_notes:
                # remove note from fretboard
                fretboard[i][j] = " "

    return fretboard

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # Check if there is a session id already
    if "user_id" not in session:
        print("NO SESSION[USER_ID] FOUND (USER NOT LOGGED IN)")
        redirect("/login")
    else:
        user_id = session["user_id"]

        # temp print
        print(f"USER_ID: {user_id} ACCESSED INDEX")

        try:
            saved_parameters = db.execute("SELECT * FROM parameters WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", user_id)
            saved_parameters = saved_parameters[0]
            print(f"SAVED_PARAMETERS: {saved_parameters}")
        except IndexError:
            # redirect the user if they have no previously saved parameters
            return redirect("/parameters")


        # Generate full fretboard (default for get request)
        fretboard = generate_fretboard(saved_parameters['string_count'], saved_parameters['fret_count'], saved_parameters['sharps_or_flats'])


        if request.method == "POST":
            print("METHOD == POST")

            selected_scale = request.form.get('scale')

            fretboard = render(fretboard, scales[selected_scale], saved_parameters['sharps_or_flats'])

            # selected_scale = request.form.get('scale')
            return render_template("index.html", string_count=saved_parameters['string_count'], fret_count=saved_parameters['fret_count'], fretboard=fretboard)
        else:

            # TODO:
            # user_id = session_id -- implement this later

            # SAVED PARAMETERS ORIGINAL PLACEMENT

            # FRETBOARD ORIGINAL PLACEMENT

            return render_template("index.html", string_count=saved_parameters['string_count'], fret_count=saved_parameters['fret_count'], fretboard=fretboard)

@app.route("/parameters", methods=["GET", "POST"])
@login_required
def parameters():

    # Check if there is a session id already
    if not session["user_id"]:
        print("NO SESSION[USER_ID] FOUND (USER NOT LOGGED IN)")
        redirect("/login")
    else:
        user_id = session["user_id"]

    if request.method == "POST":
        print("METHOD == POST")

        string_count = request.form.get('dropdown_strings')
        string_count = int(string_count)
        fret_count = request.form.get('dropdown_frets')
        fret_count = int(fret_count)
        sharps_or_flats = request.form.get('sharps_or_flats')

        # ORIGINAL PLACEMENT OF def generate_fretboard() FUNCTION
        generate_fretboard(string_count, fret_count, sharps_or_flats)

        # TODO: CHECK IF SAME SETTINGS ALREADY EXIST FOR USER
        # IF SO, RESET TIMESTAMP ON EXISTING SETTING SO IT IS AT THE FOREFRONT

        # save changes
        db.execute("INSERT INTO parameters (user_id, string_count, fret_count, sharps_or_flats) VALUES (?, ?, ?, ?)", user_id, string_count, fret_count, sharps_or_flats)

        return redirect("/")
    else:
        return render_template("parameters.html")

@app.route("/saved-parameters", methods=["GET", "POST"])
def saved_parameters():

    # Check if there is a session id already
    if not session["user_id"]:
        print("NO SESSION[USER_ID] FOUND (USER NOT LOGGED IN)")
        redirect("/login")
    else:
        user_id = session["user_id"]

    # MAY BREAK (SEE SOLUTION IN /)
    # USER SHOULD NOT BE ABLE TO ACCESS THIS PAGE BEFORE SETTING PARAMETERS ANYWAY
    saved_parameters = db.execute("SELECT * FROM parameters WHERE user_id = ?", user_id)
    # redirect the user if they have no previously saved parameters
    if len(saved_parameters) <= 0:
        return redirect("/parameters")

    print(f"SAVED_PARAMETERS (/saved-parameters): {saved_parameters}")

    if request.method == "POST":
        print("METHOD == POST")

        selected_id = request.form.get("id")

        # Update timestamp of previous parameter combination to current timestamp so it is interpeted as the user's current settings
        db.execute("UPDATE parameters SET timestamp = CURRENT_TIMESTAMP WHERE id = ?", selected_id)

        return render_template("saved-parameters.html", length=len(saved_parameters), saved_parameters=saved_parameters)

    else:
        print("ACCESSED SAVED PARAMETERS PAGE (GET METHOD)")

        # add button for each row to select settings as current settings
        # do this by setting new timestamp
        return render_template("saved-parameters.html", length=len(saved_parameters), saved_parameters=saved_parameters)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return redirect("/login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return redirect("/login")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return redirect("/login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    print("REGISTER PAGE ACCESSED")

    session.clear()

    if request.method == "POST":
        print("METHOD = POST")

        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirmation")

        if not username:
            return redirect("/register")
        elif not password or not confirm_password:
            return redirect("/register")
        elif password != confirm_password:
            return redirect("/register")
        else:
            # hash_password = generate_password_hash(password, method='pbkdf2', salt_length=16)
            hash_password = generate_password_hash(password)

             # check for same username in database, prevent duplicate names
            rows = db.execute("SELECT * FROM users WHERE username = ?", username)
            if len(rows) > 0:
                print("USERNAME ALREADY TAKEN")
                # TODO: Print same message to user
                return redirect("/register")
            else:
                db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash_password)
                return redirect("/login")  # Redirect to login after successful registration
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")
