import flask as fk
import stew_bot

app = fk.Flask(__name__,static_folder="static",template_folder="templates")

@app.route('/',methods=["GET","POST"])
def root():
    method = fk.request.method
    redditContent = "hi there!"
    posts = stew_bot.load_posts(5)
    return fk.render_template("home.html",content=redditContent,loadedPosts=posts)


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
