import os

from cs50 import SQL
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
)
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import datetime
import math

# CS50 helpers from Finance PSET Week 9
from helpers import apology, login_required

# Image Modules
from PIL import Image

# Possible Revamp
# import sqlalchemy

# TODO
# Will Implement On Personal server, Don't think Github would like it.
# from nudenet import NudeDetector

# Set it up
# nude_detector = NudeDetector()

# And to use Nude Detector in a FUNCTION,
# like say profile pic or forum
# it returns censored image ouput path
# nude_detector.censor("image.jpg")
######### Testing ############
# To see the stats of nude image probability
# nude_detector.detect("image.jpg")

# Variable for place to upload profile pic.
UPLOAD_FOLDER = "images/uploads"

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
Session(app)

# Configure use of sqlite3 connection.
db = SQL("sqlite:///data.db")


# Setup Webapp
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


################### FUNCTIONS ##################


# Function to check if a file uploaded is of type Image
def allowed_types(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {
        "png",
        "jpg",
        "jpeg",
        "gif",
    }


# Function to check if username meets criteria
def check_username(username):
    if len(username) < 8 or len(username) > 16:
        return False
    return True


# Function to check if Input is Clean NO PROFANITY
def check_profanity(input):
    # Split sentence into words list.
    words = input.split(" ")
    # Check every word in list.
    for word in words:
        # If word in profanity table
        flags = db.execute(
            "SELECT COUNT(word), COUNT(canonical_form_1), COUNT(canonical_form_2), COUNT(canonical_form_3) FROM profanity WHERE ? IN (word, canonical_form_1, canonical_form_2, canonical_form_3)",
            word.lower(),
        )
        if (
            flags[0]["COUNT(word)"] > 0
            or flags[0]["COUNT(canonical_form_1)"] > 0
            or flags[0]["COUNT(canonical_form_2)"] > 0
            or flags[0]["COUNT(canonical_form_3)"] > 0
        ):
            return False
    return True


# Function to check if password meets criteria
def check_password(password):
    l, u, d, s = 0, 0, 0, 0
    special = ["!", "@", "#", "$", "%", "&", "*", "_", ".", "?"]
    if len(password) >= 8 or len(password) <= 32:
        for i in password:
            if i.islower():
                l += 1
            if i.isupper():
                u += 1
            if i.isdigit():
                d += 1
            if i in special:
                s += 1
        if l >= 1 and u >= 1 and d >= 1 and s >= 1 and l + u + d + s == len(password):
            return True
        else:
            return False
    else:
        return False


#################### ROUTES ####################


# Registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # If http request is POST.
    if request.method == "POST":
        # Retrieve data from forms.
        name = request.form.get("name")
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Make sure username meets all Requirements.
        if check_username(username) == False:
            flash("Username must be at least 8 charactors long.")
            return redirect("/register")

        # CHECK NAME FOR PROFANITIES!
        if check_profanity(name) == False:
            flash("Please enter a Name without Profanities in it.")
            return redirect("/register")

        # CHECK USERNAME FOR PROFANITIES!
        if check_profanity(username) == False:
            flash("Please enter a Username without Profanities in it.")
            return redirect("/register")

        # Make sure password meets all Requirements.
        if check_password(password) == False:
            flash(
                "Please enter a Password with at least 1 of each Lowercase, Uppercase, Number, Special Character ! @ # $ % & * _ . ? in it."
            )
            return redirect("/register")

        # Make sure a name was entered.
        if not name:
            return apology("Please enter your name.", 400)

        # Make sure a username was entered.
        if not username:
            return apology("Please enter a username.", 400)

        # Query all usernames
        usernames = db.execute("SELECT username FROM users")

        # Make sure username doesn't already exist.
        if any(v["username"] == username for v in usernames):
            return apology("Sorry this Username is already taken.", 400)

        # Make sure both password and confirmation fields were not blank.
        if not password or not confirmation:
            return apology("Please re-enter the password in both boxes.", 400)

        # Make sure password and confirmation are a match.
        if password != confirmation:
            return apology("Both Boxes need to match, Please try again.", 400)

        # Hash the password for encrypted value.
        hashed = generate_password_hash(password)

        # Get current date and time.
        dt = datetime.datetime.now()

        # Store the hashed password and username in table.
        db.execute(
            "INSERT INTO users (name, username, hash, last_log_in) VALUES(?, ?, ?, ?)",
            name,
            username,
            hashed,
            dt.strftime("%m-%d-%Y"),
        )

        # Flash message.
        flash("Successfully registered as " + username)

        # Redirect to login.
        return render_template("login.html")

    # Else http request is GET.
    else:
        return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id.
    session.clear()

    # User reached route via POST (as by submitting a form via POST).
    if request.method == "POST":
        # Ensure username was submitted.
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted.
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username.
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct.
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in.
        session["user_id"] = rows[0]["id"]

        # Get current date and time.
        dt = datetime.datetime.now()

        # Update users table with the last time user logged in, so we can delete them after 10 years of (no cookie use?).
        db.execute(
            "UPDATE users SET last_log_in = ? WHERE id = ?",
            dt.strftime("%x"),
            session["user_id"],
        )

        # Flash message.
        flash("Welcome")

        # Redirect user to home page.
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect).
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Flash message
    flash("Logged Out")

    # Redirect user to login form
    return redirect("/")


@app.route("/settings", methods=["GET", "POST"])
def change():
    """Change settings"""

    # If http request is POST.
    if request.method == "POST":
        # Retrieve data from forms.
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Get hash of user.
        password_query = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"]
        )[0]["hash"]

        # Make sure a username was entered.
        if not current_password or not check_password_hash(
            password_query, current_password
        ):
            flash("Please re-enter your current password.")
            return render_template("settings.html")

        # Make sure both password and confirmation fields were not blank.
        if not new_password or not confirmation:
            return apology("Please re-enter the password in both boxes.", 400)

        # Make sure password and confirmation are a match.
        if new_password != confirmation:
            return apology("Both Boxes need to match, Please try again.", 400)

        # Update database with new password.
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            generate_password_hash(new_password),
            session["user_id"],
        )

        # Flash message
        flash("Password Updated")

        # Redirect to login
        return redirect("/logout")

    # Else http request is GET.
    else:
        return render_template("settings.html")


@app.route("/")
def index():
    # Render Index (HOME) Page
    return render_template("index.html")


@app.route("/launches")
def launches():
    # Render Launches Page
    return render_template("launches.html")


@app.route("/events")
def events():
    # If Post method
    if request.method == "POST":
        # Retrieve data from forms.
        birthday = request.form.get("birthday")
        contact = request.form.get("contact")
        password = request.form.get("password")
        role = request.form.get("role")

        # Make sure all fields were entered.
        if not password or not birthday or not contact:
            return apology("Please enter info in all fields.", 400)

        # Get hash of user.
        password_query = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"]
        )[0]["hash"]

        # Make sure a username was entered.
        if not password or not check_password_hash(password_query, password):
            flash("Please re-enter your password.")
            return render_template("settings.html")

        # Get username from database.
        name = db.execute("SELECT name FROM users WHERE id = ?", session["user_id"])

        # Store the hashed password and username in table.
        db.execute(
            "INSERT INTO volunteers (name, birthday, role, contact) VALUES(?, ?, ?, ?)",
            name,
            birthday,
            role,
            contact,
        )

    else:
        # Load choices for volunteer roles
        choices = ["Planning", "Trash Clean Ups", "Yaxi Driver", "Game Ref"]

        return render_template("events.html", choices=choices)


@app.route("/mission")
def mission():
    # Render Mission Page.
    return render_template("mission.html")


@app.route("/about")
def about():
    # Render About Page.
    return render_template("about.html")


@app.route("/forum", methods=["GET", "POST"])
@app.route("/forum/")
@login_required
def forum():
    # Number of comments per page.
    posts_per_page = 15

    # If someone submitted a comment.
    if request.method == "POST":
        # Retrieve comment.
        comment = request.form.get("comment_post")

        # If not comment is empty or not none.
        if comment or len(comment) > 0:
            # Replace profane words in comment.
            safe_comment = ""
            # Split sentence into words list.
            words = comment.split(" ")
            # Check every word in list.
            for word in words:
                # If word in profanity table.
                # TODO Run function check_profanity instead of redundancy.
                flags = db.execute(
                    "SELECT COUNT(word), COUNT(canonical_form_1), COUNT(canonical_form_2), COUNT(canonical_form_3) FROM profanity WHERE ? IN (word, canonical_form_1, canonical_form_2, canonical_form_3)",
                    word.lower(),
                )
                if (
                    flags[0]["COUNT(word)"] > 0
                    or flags[0]["COUNT(canonical_form_1)"] > 0
                    or flags[0]["COUNT(canonical_form_2)"] > 0
                    or flags[0]["COUNT(canonical_form_3)"] > 0
                ):
                    replace = ""
                    # Make every letter in word a *.
                    for letter in word:
                        replace += "*"
                    # Update comment with all *'s.
                    safe_comment += replace + " "
                # Word is safe.
                else:
                    # Add word to new safe comment.
                    safe_comment += word + " "

            # Get user name.
            username = db.execute(
                "SELECT username FROM users WHERE id = ?", session["user_id"]
            )[0]["username"]

            # Get the date and time for right now.
            dt = datetime.datetime.now()

            # Add comment to comment table.
            db.execute(
                "INSERT INTO comments (username, comment, date, time) VALUES(?, ?, ?, ?)",
                username,
                safe_comment,
                dt.strftime("%x"),
                dt.strftime("%X"),
            )
            # Reload the forum.
            return redirect("/forum")

    # GET method Or reload after comment posted.
    else:
        # Get total count of comments.
        count = db.execute("SELECT COUNT(comment_id) FROM comments")[0][
            "COUNT(comment_id)"
        ]
        # Do the math to figure out how many pages total.
        pages = math.ceil(float(count / posts_per_page))
        # Get current page number if relevent.
        page = request.args.get("page")
        if page and page != None:
            # This make sure its a positive number only.
            if page.isdigit():
                # Make sure page is a number between 1 and total pages.
                if int(page) == 0 or int(page) > pages:
                    return apology("Sorry No Page with that number.", 400)
                # Get Start and End positions for query of page comments.
                else:
                    end = count - (int(page) - 1) * posts_per_page
                    start = end - posts_per_page
                    if start < 0:
                        start == 0
            # Must not have been a Positive number.
            else:
                return apology("Thats NOT a valid Page Number", 400)
        # No current page yet so do the math for start and end for page 1.
        else:
            page = 1
            end = count
            start = count - posts_per_page

        # Reinventing the wheel:) Pagination.
        if int(page) + 4 <= pages:
            pagination = 4
        elif int(page) + 3 <= pages:
            pagination = 3
        elif int(page) + 2 <= pages:
            pagination = 2
        elif int(page) + 1 <= pages:
            pagination = 1
        else:
            pagination = 0

        # Get comments from data base.
        comments = db.execute(
            "SELECT * FROM comments WHERE comment_id BETWEEN ? AND ? ORDER BY comment_id DESC LIMIT ?",
            start,
            end,
            posts_per_page,
        )

        # Get profile picture for each commenter to display in comment.
        for row in comments:
            name = row.get("username")
            pic = db.execute("SELECT picture FROM users WHERE username = ?", name)
            if not pic or pic == None:
                row["picture"] = "images/anon.png"
            else:
                row["picture"] = pic[0]["picture"]

        # Load Forum Page.
        return render_template(
            "forum.html",
            comments=comments,
            pages=pages,
            page=page,
            pagination=pagination,
        )


@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    # If Post method.
    if request.method == "POST":
        # Check for part file.
        if "profile_pic" not in request.files:
            flash("No file part.")
            return redirect("/settings")

        # Retrieve picture.
        picture = request.files["profile_pic"]

        # Check for filename.
        if picture.filename == "":
            flash("No file.")
            return redirect("/settings")

        # Retrieve username from database.
        username = db.execute(
            "SELECT username FROM users WHERE id = ?", session["user_id"]
        )[0]["username"]

        # Make sure there is a picture and it is a picture type.
        if picture and allowed_types(picture.filename):
            # File name security.
            filename = secure_filename(picture.filename)

            # TODO Nudity Filter using nudenet module.

            # Open picture and resize.
            picture = Image.open(picture)
            picture = picture.resize((100, 100))

            # Variable for Path.
            new_path = UPLOAD_FOLDER + "/" + username
            static = "static/"
            # If no folder named "username" exists in uploads folder.
            if os.path.exists(static + new_path) == False:
                print("here")
                # Create username folder.
                os.mkdir(static + new_path)
            # If Image doesn't exist.
            if os.path.exists(static + new_path + "/" + filename) == False:
                print("here1")
                # And if folder is empty.
                if os.listdir(static + new_path) == []:
                    print("here2")
                    # Save image as lower quality.
                    picture.save(os.path.join(static + new_path, filename))
                # Folder not empty so lets empty it.
                else:
                    print("here3")
                    try:
                        for root, dirs, files in os.walk(static + new_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                os.remove(file_path)
                                # Now save in emptied folder.
                                picture.save(os.path.join(static + new_path, filename))
                    # Something went wrong with emptying folder.
                    except OSError:
                        flash("System Error Uploading Image.")
                        return render_template("settings.html")
            # Image must already exist.
            else:
                flash("That image already exists")
                return render_template("settings.html")
        # File type not allowed or no pic
        else:
            flash("Sorry that file type is not allowed.")
            return render_template("settings.html")
        # UPDATE users Table with picture location.
        db.execute(
            "UPDATE users SET picture = ? WHERE username = ?",
            new_path + "/" + filename,
            username,
        )

        # Success everything when well.
        flash("Picture Successfully Uploaded.")
        # Load page with new profile pic near upload area.
        return render_template("settings.html", new_path=new_path + "/" + filename)

    # GET request to upload so just redirect settings, nothing to see here.
    else:
        return render_template("settings.html")


@app.route("/game")
def game():
    # Render Launches Page.
    return render_template("game.html")


@app.route("/deregister", methods=["GET", "POST"])
def deregister():
    """Deregister user"""
    # If Post method.
    if request.method == "POST":
        # Retrieve data from forms.
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation2")

        # Get hash of user.
        password_query = db.execute(
            "SELECT hash FROM users WHERE id = ?", session["user_id"]
        )[0]["hash"]

        # Make sure a username was entered.
        if not password or not check_password_hash(password_query, password):
            flash("Please re-enter your password.")
            return render_template("settings.html")

        # Make sure both password and confirmation fields were not blank.
        if not password or not confirmation:
            return apology("Please enter your password in both boxes.", 400)

        # Make sure password and confirmation are a match.
        if password != confirmation:
            return apology("Both Password Boxes need to match, Please try again.", 400)

        # Update database with new password.
        db.execute("DELETE FROM users WHERE id = ?", session["user_id"])

        # Logout of session.
        session.clear()

        # Flash message.
        flash("Your User account has been removed.")
        return redirect("/")
    # Can't Deregister this way.
    else:
        return redirect("/logout")


# Trick to running app with "python app.py"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
