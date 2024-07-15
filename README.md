# Ladle
<img src="static/images/LadleApp.png" width="128" alt="Ladle Logo">

**Ladle** is a dynamic application that brews together top news, notable specified subreddit posts, and interesting topics without the clutter of the app, for local use.

Quickly peek at **r/popular** or cook up your own feed.

## Features
- Pick interesting subreddits to follow
  - Select predefined lists or brew up your own
- Search through top stories
  - Clearly demarcated upvote counts/ratios, subreddit titles, comment trees and more
- Utilize a simple interface to navigate posts, get quick info on subreddits, and peek at users
  - Open Reddit for post specifics
- Simple searches in subreddits, user pages, and the website

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

* [Praw](https://praw.readthedocs.io/en/stable/index.html) for Reddit API
* [Flask](https://flask.palletsprojects.com/en/latest/) and Jinja
* HTML/CSS
* **Libraries**: nh3, markdown, json, requests, datetime, dotenv, config

Check out Reddit API Wiki for developer account setup: [API](https://www.reddit.com/wiki/api/) 

### Plans
**Version 1 Plans**
- **Pagination** for posts on homepage and for recent comments / posts on user
  - [paginate, stackoverflow](https://stackoverflow.com/questions/33556572/paginate-a-list-of-items-in-python-flask)
- Use **INFO** api method for calls
  - [praw.Reddit.info](https://praw.readthedocs.io/en/stable/code_overview/reddit_instance.html#praw.Reddit.info)
- Add testing suite for app
  - [flask_tests](https://flask.palletsprojects.com/en/3.0.x/testing/#identifying-tests)   
- Profile application for speed improvements
  - time.time, flask_profiler
- Simple search on user or subreddit page and home
- Comment tree rendering, load comments
- Create simple rundown for running app
- Host exemplary version
  * Try [pythonanywhere](https://www.pythonanywhere.com/)

**Version 2 Plans**
- Add the *ability* to save posts, or take notes on posts once logged in
  - Praw save feature or user's db
- Add user login / logout features to store custom feed profiles?
- Add possible SQL Alchemy DB for posts
  - [SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/)
- Render a loading page (json fetching?) until content is done loading
- Add command line job availability or auto-running capabilities
  - FastAPI for Ladle
- Take a look at ASYNC loading 
  * [Async Praw](https://asyncpraw.readthedocs.io/en/stable/code_overview/models/submission.html)
- Render **videos** after a button is clicked, poll data and galleries on posts

## License

Ladle uses the [GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license
