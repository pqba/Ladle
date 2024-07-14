import stew_bot
import flask as fk
from flask import session
from flask_caching import Cache
import datetime
from dotenv import load_dotenv
from os import environ
import requests
import json
from markdown import markdown

load_dotenv()

app = fk.Flask(__name__, static_folder="static", template_folder="templates")

cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# Cache timeout values for pages, in seconds
LONG_TIMEOUT = 1800
SHORT_TIMEOUT = 600

# Configure Session
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['SESSION_TYPE'] = 'filesystem'

if not app.config['SECRET_KEY']:
    raise ValueError("SECRET_KEY environment variable is not set!")

sub_profiles = {
    "cs+math": ["math", "machinelearning", "computerscience", "calculus", "askmath"],
    "music": ["piano", "audiophile", "guitar", "musictheory", "wearethemusicmakers"],
    "arts": ["art", "design", "diy", "painting", "photography"],
    "health": ["fitness", "nutrition", "yoga", "weightlifting", "meditation"],
    "sports": ["sports", "nba", "soccer", "nfl", "mls"],
    "default": ["popular"]
}


@app.route('/', methods=["GET", "POST"])
def root(loaded_posts=None):
    if 'content' not in fk.session:
        fk.session["content"] = sub_profiles["default"]
    current_date = str(datetime.date.today())
    if not loaded_posts:
        loaded_posts = stew_bot.load_posts(10, fk.session["content"])
        remember_post_id(loaded_posts)

    return fk.render_template("home.html", date=current_date, loadedPosts=loaded_posts)


# Renders sub_form and gets inputted values, clears cache
@app.route('/subreddit_list', methods=["GET", "POST"])
def get_subs():
    if fk.request.method == "POST":
        # Access form data
        sub_1 = fk.request.form.get("sub_1")
        sub_2 = fk.request.form.get("sub_2")
        sub_3 = fk.request.form.get("sub_3")
        sub_4 = fk.request.form.get("sub_4")
        sub_5 = fk.request.form.get("sub_5")
        subs_raw = [sub_1, sub_2, sub_3, sub_4, sub_5]
        subs = [s for s in subs_raw if s != "."]  # '.' means no sub
        # Validate Form
        if len(subs) > 0 and valid_subs(subs):
            fk.session["content"] = subs
            cache.clear()
            return fk.redirect("/")
        else:
            err_msg = "Please choose a valid subreddit configuration or enter valid subreddit(s) in the form."
            return fk.render_template("sub_form.html", err_choose=err_msg, err_btns="")
    else:
        return fk.render_template("sub_form.html", err_choose="", err_btns="")


# Renders homepage after button selected and clears cache, error if invalid
@app.route("/subreddit_button", methods=["POST"])
def get_sub_btn():
    selection = fk.request.form["btn_sub"]
    if not valid_sub_btn(selection):
        return fk.render_template("sub_form.html", err_choose="",
                                  err_btns="Invalid button choice. Choose a preset configuration from the buttons "
                                           "below.")
    cache.clear()
    fk.session["content"] = sub_profiles[selection]
    return fk.redirect("/")


@app.route("/about", methods=["GET"])
def about():
    return fk.render_template("about.html")


# TODO: add pagination
# Renders 10 more posts on home page, hiding old content and storing new content. Clears cache
@app.route("/more-posts", methods=["GET", "POST"])
def additional_posts():
    if 'posts' not in fk.session:
        return fk.redirect("/")
    cache.clear()
    for submission_str in fk.session["posts"]:
        stew_bot.mark_seen(submission_str)

    new_content = stew_bot.load_posts(10, fk.session["content"])
    remember_post_id(new_content)
    return root(loaded_posts=new_content)


# Renders post given ID, 404 if invalid
@app.route("/post/<p_id>", methods=["GET"])
@cache.memoize(timeout=LONG_TIMEOUT)
def get_post(p_id):
    info = stew_bot.post_info(p_id)
    if info is None:
        e = stew_bot.clean(f"Post doesn't exist or Ladle cannot find post id: {p_id}.")
        return page_not_found(e)
    post_created = to_ymd(info['utc'])
    md_text = markdown(info['text'])
    img_post = info['url'][8] == 'i'  # 'https://i'  is how image posts are formatted
    return fk.render_template("post.html", info=info, u_icon=info['by-icon'], p_date=post_created, p_url=info['url'],
                              p_text=md_text, img_post=img_post)


# Renders user info page, 404 if deleted or invalid
@app.route("/user/<name>", methods=["GET"])
@cache.memoize(timeout=SHORT_TIMEOUT)
def get_user(name):
    person = stew_bot.user_info(name)
    if person is None:
        e = stew_bot.clean(f"User doesn't exist or Ladle cannot find u/{name}.")
        return page_not_found(e)
    user_created = to_ymd(person['utc'])
    # For now only gather most recent 3 posts. 
    # TODO: implement pagination
    person["comments"] = person["comments"][:4]
    person["posts"] = person["posts"][:4]
    return fk.render_template("user.html", person=person, person_icon=person['icon'], person_made=user_created)


# Renders subreddit,formats subs with commas, 404 if invalid name
@app.route("/subreddit/<sub_name>")
@cache.memoize(timeout=LONG_TIMEOUT)
def get_sub(sub_name):
    sub = stew_bot.subreddit_info(sub_name)
    if sub is None:
        e = stew_bot.clean(f"Subreddit doesn't exist or Ladle cannot find r/{sub_name}.")
        return page_not_found(e)
    sub_created = to_ymd(sub['utc'])
    sub['subs'] = f"{sub['subs']:,}"  # Comma separated
    # TODO: render loaded data
    #  sub_extra = subreddit_info(sub_name)
    sub_extra = {}
    return fk.render_template("subreddit.html", subreddit=sub, subreddit_created=sub_created, subreddit_bg="",
                              subreddit_icon="",subreddit_extra=sub_extra)


# Returns icon, banner, active users, and category of sub
def subreddit_info(sub_name: str):
    url = f"https://www.reddit.com/r/{sub_name}/about.json"
    req = requests.get(url)

    parsed = json.loads(req.text)["data"]
    if 'error' in parsed:  # For: {'message': 'Too Many Requests', 'error': 429}
        return None

    # print(json.dumps(parsed, indent=4))

    sub_info = {
        'subtitle': parsed['title'],
        'header_title': parsed['header_title'],
        'active': parsed['accounts_active'],
        'category': parsed['advertiser_category'],
        'lang': parsed['lang'],
        # Icons/banners are in 2 different styles, removing possible '?' fixes image links.
        'icon': parsed['icon_img'].split("?")[0],
        'bannerA': parsed['banner_img'].split("?")[0],
        'bannerB': parsed['banner_background_image'].split("?")[0]
    }
    print(f"PARSED JSON DATA FOR r/{sub_name}:\n{sub_info}\n")
    # Other interesting fields: description(the full long post), submit_text, mobile_banner_image,
    # quarantine, and header_img
    return sub_info


# Converts UTC timestamp to YMD format
def to_ymd(utc: float) -> str:
    date_time = datetime.datetime.fromtimestamp(utc)
    when = date_time.strftime('%Y-%m-%d')
    return when


# Stores post list in session variable
def remember_post_id(reddit_posts: list) -> None:
    post_list = [str(p[-1]) for p in reddit_posts]
    fk.session["posts"] = post_list


# Make sure list of subs is valid and > 1
def valid_subs(sub_list: list[str]) -> bool:
    for subreddit in sub_list:
        if not subreddit or subreddit == "":
            return False
        if not stew_bot.sub_exists(subreddit):
            return False
    return True


# Ensure button name is a valid configuration
def valid_sub_btn(btn_name: str) -> bool:
    return btn_name in sub_profiles.keys()


@app.errorhandler(404)
def page_not_found(e=""):
    return fk.render_template('404.html', error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    # note that we set the 500 status explicitly
    return fk.render_template('500.html', error=e), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7150)
