import flask as fk
from flask_session import Session
import stew_bot
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()

app = fk.Flask(__name__, static_folder="static", template_folder="templates")

# Configure Session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY environment variable is not set!")
Session(app)

sub_profiles = {
    "cs+math": ["math", "machinelearning", "computerscience", "calculus", "askmath"],
    "music": ["piano", "audiophile", "guitar", "musictheory"],
    "arts": ["art", "design", "diy", "painting", "photography"],
    "health": ["fitness", "nutrition", "yoga", "weightlifting", "meditation"],
    "sports": ["sports", "nba", "soccer", "nfl", "mls"]
}

# Official Subreddit Selection
sublist = ["piano", "guitar", "classicalmusic", "learnprogramming", "computerscience", "machinelearning", "math"]

@app.route('/', methods=["GET", "POST"])
def root():
    if 'content' not in fk.session:
        fk.session["content"] = sublist
    current_date = str(date.today())
    posts = stew_bot.relevant_info(stew_bot.load_posts(10, fk.session["content"]))
    return fk.render_template("home.html", date=current_date, loadedPosts=posts)


@app.route('/subreddit_list', methods=["GET", "POST"])
def get_subs():
    if fk.request.method == "POST":
        # Access form data
        sub_1 = fk.request.form.get("sub_1")
        sub_2 = fk.request.form.get("sub_2")
        sub_3 = fk.request.form.get("sub_3")
        sub_4 = fk.request.form.get("sub_4")
        sub_5 = fk.request.form.get("sub_5")
        subs = [sub_1, sub_2, sub_3, sub_4, sub_5]
        # Validate Form
        if valid_subs(subs):
            fk.session["content"] = subs
            return fk.redirect("/")
        else:
            err_msg = "Please choose a valid subreddit or enter valid subreddits in the form."
            return fk.render_template("sub_form.html", err=err_msg)
    else:
        return fk.render_template("sub_form.html", err="")

@app.route("/about",methods=["GET"])
def about():
    return fk.render_template("about.html")

# Make sure list of subs is full and actual subreddits
def valid_subs(sublist: list[str]):
    for subreddit in sublist:
        if not subreddit or subreddit == "":
            return False
        if not stew_bot.sub_exists(subreddit):
            return False
    return True


@app.errorhandler(404)
def page_not_found(e):
    return fk.render_template('404.html'), 404

# Ensure responses aren't cached (used from CS50 finance)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
