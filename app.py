import flask as fk
import stew_bot
from datetime import date

app = fk.Flask(__name__, static_folder="static", template_folder="templates")


@app.route('/', methods=["GET", "POST"])
def root():
    current_date = str(date.today())
    # Eventually redirect to the sub_form...
    sublist = ["piano", "guitar", "classicalmusic", "learnprogramming", "computerscience", "machinelearning", "math"]
    posts = stew_bot.relevant_info(stew_bot.load_posts(10, sublist))
    return fk.render_template("home.html", date=current_date, loadedPosts=posts)


@app.route('/subreddit_list', methods=["GET", "POST"])
def get_subs():
    if fk.request.method == "POST":
        # Access form data
        sub_1 = fk.request.form["sub_1"]
        sub_2 = fk.request.form["sub_2"]
        sub_3 = fk.request.form["sub_3"]
        sub_4 = fk.request.form["sub_4"]
        sub_5 =  fk.request.form["sub_5"]
        subs = [sub_1,sub_2,sub_3,sub_4,sub_5]
        # store subs in cookies at some point...
        return fk.redirect(fk.url_for('root'))
    else:
        # Render the form
        return fk.render_template("sub_form.html")


@app.errorhandler(404)
def page_not_found(e):
    return fk.render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
