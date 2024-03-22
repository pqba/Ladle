# Ladle

<img src="images/LadleApp.png" width="512" alt="Ladle Logo">

**Ladle** is a dynamic bot that brews together top news, notable specified subreddit posts, and interesting topics without the clutter or doomscroll from visiting the website. 

- Pick interesting subreddits to follow
- Search through top stories
- Utilize a simple interface to navigate posts
- Open Reddit for more details if necessary

## Run
Project Structure
```
.
├── README.md
├── app.py
├── images
│   └── LadleApp.png
├── praw.ini
├── requirements.txt
├── static
│   └── stylesheets
│       └── style.css
├── stew_bot.py
└── templates
    ├── base.html
    └── home.html
```

To set up virtual environment
```
python3 -m venv myenv
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

To execute Ladle
```
python3 stew_bot.py
```

To test Flask App 
```
flask --app app run
```
Open: http://127.0.0.1:5000

## Documentation

Refer to Praw Documentation for more info [Praw](https://praw.readthedocs.io/en/stable/index.html)

## Goals
- Build in basic error handling for script
- Gather necessary data, simplify pipeline
- Create overlying Flask App to render Ladle with good UI
- Add command line job availability or auto-running capabilities
- Create simple documentation

## License

Ladle uses the [MIT License](https://opensource.org/license/mit)
