import praw
import os

# Documentation: https://praw.readthedocs.io/en/stable/
# Inspiration: https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html

# Bot Name: u/theLadled
def load_ladle()->praw.Reddit:
        reddit= praw.Reddit("LadleBot")
        return reddit

def main():
    reddit = load_ladle()

    print(reddit.user.me())

    sub_list = ["piano","guitar","classicalmusic","learnprogramming","computerscience","math"]

    search = ""
    for sub in sub_list[:-1]:
        search += sub + "+"
    search += sub_list[-1]


    for submission in reddit.subreddit(search).hot(limit=25):
        print(f"{submission.title} {submission.upvote_ratio} {submission.url}")

if __name__ == "__main__":
    main()