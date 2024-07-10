# Ladle
<img src="static/images/LadleApp.png" width="128" alt="Ladle Logo">

**Ladle** is a dynamic application that brews together top news, notable specified subreddit posts, and interesting topics without the clutter of the app, for local use.

Quickly peek at the default **r/popular** for a specific country or curate a specific sub interest list. 

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

> For caching, Flask **Sessions** are used. In the `.env` file use a properly secured key for production.

## Technology and Documentation

* Praw for Reddit API
* nh3 for input sanitization, markdown for MD rendering
* Flask and Jinja
* HTML/CSS

[Flask Docs](https://flask.palletsprojects.com/en/latest/)

[Praw Docs](https://praw.readthedocs.io/en/stable/index.html)

Check out Reddit API Wiki for developer account setup: [API](https://www.reddit.com/wiki/api/) 

### Goals
- Build in basic error handling for script (500 errors)
- Speed up rendering / fetching time or use async
- Render a loading page (json fetching?) until content is done loading
- Simplify data pipeline
- Simple search on user,post, or subreddit page
  * Manage cookies / login or logout of basic profiles
- Comment tree rendering, load comments
- Inspect user profiles
- Take a look at ASYNC loading 
  * https://asyncpraw.readthedocs.io/en/stable/code_overview/models/submission.html
- Add command line job availability or auto-running capabilities
- Create simple documentation for self-hosting
- Host exemplary version
  * Use [pythonanywhere](https://www.pythonanywhere.com/)

## License

Ladle uses the [GPLv3](https://choosealicense.com/licenses/gpl-3.0/) license
