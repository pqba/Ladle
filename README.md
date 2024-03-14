# Ladle

![Ladle App Icon](images/LadleApp.png "Ladle Logo")

Ladle is a dynamic bot that brews together top news, notable specified subreddit posts, and interesting topics without the clutter of visiting the website. 

- Pick Interesting Subreddits to follow
- Search through top stories
- A simple UI to navigate posts

## Run
Project Structure
```
.
├── README.md
├── images
│   └── LadleApp.png
├── praw.ini
├── requirements.txt
└── stew_bot.py
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

To run Ladle
```
python3 stew_bot.py
```

## Documentation

Refer to Praw Documentation for more info [Praw](https://praw.readthedocs.io/en/stable/index.html)

## Goals
- Build in basic error handling for script
- Gather necessary data, simplify pipeline
- Create overlying Flask App to render Ladle
- Add command line job availability or auto-running capabilities
- Create simple documentation

## License

Ladle uses the [MIT License](https://opensource.org/license/mit)