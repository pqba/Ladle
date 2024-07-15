# Ladle
<img src="static/images/LadleApp.png" width="128" alt="Ladle Logo">

**Ladle** is a dynamic application that brews together top news, notable specified subreddit posts, and interesting topics without the clutter of the app, for local use.

Quickly peek at **r/popular** or make your own feed.

## Features
UI and design methodology is based on [hackernews](https://news.ycombinator.com/) 
- Pick interesting subreddits to follow
  - Select predefined lists or brew up your own
- Search through top stories
  - Clearly demarcated upvote counts/ratios, subreddit titles, comment trees and more
- Utilize a simple interface to navigate posts, get quick info on subreddits, and peek at users
- Open Reddit for post specifics

## Run
Set up virtual environment
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

Create and configure a `praw.ini` file by inputting
- client_id, client_secret, username, password, and user_agent

> [.ini Documentation](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html)

Change other configurations in default or add more bots as necessary.


### Backend functionality
```bash
python3 stew_bot.py
```

### Frontend app
```bash
flask --app app run
```

> Flask's Sessions and Cache are used to store data. In the `.env` file use a properly secured key for production.

## Technology and Documentation

* Praw for Reddit API
* nh3 for input sanitization, markdown for rendering
* Flask and Jinja
* HTML/CSS
* [Flask Docs](https://flask.palletsprojects.com/en/latest/)
* [Praw Docs](https://praw.readthedocs.io/en/stable/index.html)

Check out Reddit API Wiki for developer account setup: [API](https://www.reddit.com/wiki/api/) 

### Plans
- **Pagination** for posts on homepage and for recent comments / posts on user
  - [paginate, stackoverflow](https://stackoverflow.com/questions/33556572/paginate-a-list-of-items-in-python-flask)
- Use `about.json` for subreddits to render information
- Use **INFO** api method for calls
  - [praw.Reddit.info](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit.info)
- Add possible SQL Alchemy DB for posts
  - [SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- Add testing suite for app
  - [flask_tests](https://flask.palletsprojects.com/en/3.0.x/testing/#identifying-tests)   
- Profile application for speed improvements
  - time.time, flask_profiler
- Render a loading page (json fetching?) until content is done loading
- Simple search on user,post, or subreddit page
  * Manage cookies / login or logout of basic profiles
- Comment tree rendering, load comments
- Simple search queries in subreddits and home
  - https://www.reddit.com/dev/api/#GET_search
- use pushshift
  - https://github.com/pushshift/api 
- Take a look at ASYNC loading 
  * [Async Praw](https://asyncpraw.readthedocs.io/en/stable/code_overview/models/submission.html)
- Add command line job availability or auto-running capabilities
- Create simple documentation for self-hosting
- Host exemplary version
  * Use [pythonanywhere](https://www.pythonanywhere.com/)

## License

Ladle uses the [GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license
