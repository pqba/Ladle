import flask as fk
from flask import session
import stew_bot
import datetime
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

app = fk.Flask(__name__, static_folder="static", template_folder="templates")

# Configure Session
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY environment variable is not set!")

sub_profiles = {
    "cs+math": ["math", "machinelearning", "computerscience", "calculus", "askmath"],
    "music": ["piano", "audiophile", "guitar", "musictheory","wearethemusicmakers"],
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
    current_date = str(datetime.date.today())
    
    loaded_posts = stew_bot.load_posts(10,fk.session["content"])
    remember_posts(loaded_posts)
    posts = stew_bot.relevant_info(loaded_posts)
    
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

@app.route("/more-posts",methods=["GET","POST"])
def additional_posts():
    if 'posts' not in fk.session:
        return fk.redirect("/")
    for submission_str in fk.session["posts"]:
        stew_bot.mark_seen(submission_str)

    new_content = stew_bot.load_posts(10,fk.session["content"])
    remember_posts(new_content)
    current_date = str(datetime.date.today())
    new_posts = stew_bot.relevant_info(new_content)
    return fk.render_template("home.html",date=current_date,loadedPosts=new_posts)

@app.route("/post/<id>",methods=["GET"])
def get_post(id):
    info = stew_bot.post_info(id)
    if info is None:
        e = stew_bot.clean(f"Post doesn't exist or Ladle cannot find post id: {id}.")
        return page_not_found(e)
    post_created = to_ymd(info['utc'])
    return fk.render_template("post.html",info=info,u_icon=info['by-icon'],p_date=post_created,p_url=info['url'])

@app.route("/user/<name>",methods=["GET"])
def get_user(name):
    person = stew_bot.user_info(name)
    if person is None:
        e = stew_bot.clean(f"User doesn't exist or Ladle cannot find u/{name}.")
        return page_not_found(e)
    user_created = to_ymd(person['utc'])
    return fk.render_template("user.html",person=person,person_icon=person['icon'])

@app.route("/subreddit/<sub_name>")
def get_sub(sub_name):
    sub = stew_bot.subreddit_info(sub_name)
    if sub is None:
        e = stew_bot.clean(f"Subreddit doesn't exist or Ladle cannot find r/{sub_name}.")
        return page_not_found(e)
    sub_created = to_ymd(sub['utc'])
    # TODO: parse more from about.json 
    # about = subreddit_about(sub_name)
    return fk.render_template("subreddit.html",subreddit=sub,subreddit_created=sub_created,subreddit_bg="",subreddit_icon="")

def subreddit_about(sub_name:str):
    url = f"https://www.reddit.com/r/{sub_name}/about.json"
    # Getting {'message': 'Too Many Requests', 'error': 429}
    req = requests.get(url)
    parsed = json.loads(req.text)
    print(f"PARSED JSON DATA FOR r/{sub_name}: {parsed}")
    return parsed


def to_ymd(utc:str):
    date_time = datetime.datetime.fromtimestamp(utc)
    when = date_time.strftime('%Y-%m-%d')
    return when
def remember_posts(reddit_posts:list):
    post_list = [str(p[0].id) for p in reddit_posts]
    fk.session["posts"] = post_list

# Make sure list of subs is full and actual subreddits
def valid_subs(sublist: list[str]):
    for subreddit in sublist:
        if not subreddit or subreddit == "":
            return False
        if not stew_bot.sub_exists(subreddit):
            return False
    return True


@app.errorhandler(404)
def page_not_found(e=""):
    return fk.render_template('404.html',error=e), 404

# Ensure responses aren't cached (used from CS50 finance)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7150,debug=True)
