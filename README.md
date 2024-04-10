# Ladle

<img src="images/LadleApp.png" width="512" alt="Ladle Logo">

**Ladle** is a dynamic bot that brews together top news, notable specified subreddit posts, and interesting topics without the clutter or doomscroll from visiting the website. 

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

To set up virtual environment
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To configure up ```praw.ini``` file simply place in your actual:
- client_id
- client_secret
- username
- password
- user_agent

Change other configurations in default or add more bots as necessary.

To execute base Ladle functionality
```
python3 stew_bot.py
```

To run frontend application
```
flask --app app run
```
Open: http://127.0.0.1:5000 on local machine

## Documentation

Refer to Praw Documentation for more info:  [Praw Docs](https://praw.readthedocs.io/en/stable/index.html)\
Check out Reddit API Wiki for developer account setup: [API](https://www.reddit.com/wiki/api/) 

## Goals
- Build in basic error handling for script
- Gather necessary data, simplify pipeline
- * Scrolling, open Reddit, Comment Rendering, individual posts webpage 
- Create overlying Flask App to render Ladle with good UI
- Add command line job availability or auto-running capabilities
- Create simple documentation for self-hosting
- Host examplary static version

## License

Ladle uses the [MIT License](https://opensource.org/license/mit)
