# Ladle

<img src="static/images/LadleApp.png" width="256" alt="Ladle Logo">

**Ladle** is a dynamic application that brews together top news, notable specified subreddit posts, and interesting topics without the clutter or doomscroll from visiting the website. 

Quickly peek at the default **r/popular** for a specific country or curate a specific sub interest list. 

## Features
Ladle is based on the effective and minimalistic UI for [hackernews](https://news.ycombinator.com/) but with Reddit content
- Pick interesting subreddits to follow
  - Select predefined lists or brew up your own
- Search through top stories
  - Clearly demarcated upvote counts/ratios, subreddit titles and more
- Utilize a simple interface to navigate posts
  - Scroll through comment trees, expanding in as necessary
- Open Reddit for post specifics

## Run
Set up virtual environment
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

Create and configure a `praw.ini` file by inputting
> [.ini Documentation](https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html)

- client_id
- client_secret
- username
- password
- user_agent

Change other configurations in default or add more bots as necessary.

Backend functionality
```bash
python3 stew_bot.py
```

Frontend app
```bash
flask --app app run
```
Open: http://127.0.0.1:5000 on local machine

> For caching, Flask **Sessions** are used. In the `.env` file use a properly secured key for production.

## Documentation

Refer to Praw Documentation for more info:  [Praw Docs](https://praw.readthedocs.io/en/stable/index.html)\
Check out Reddit API Wiki for developer account setup: [API](https://www.reddit.com/wiki/api/) 

### Goals
- Build in basic error handling for script (500 errors)
- Render a loading page (json fetching?) until content is done loading
- Simplify data pipeline
- * Manage cookies / login or logout of basic profiles
- Comment tree rendering, load comments
- Inspect user profiles
- Add command line job availability or auto-running capabilities
- Create simple documentation for self-hosting
- Host examplary version
- * Use [pythonanywhere](https://www.pythonanywhere.com/)


## License

Ladle uses the [MIT License](https://opensource.org/license/mit)
