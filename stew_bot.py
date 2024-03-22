import praw
import os

# Documentation: https://praw.readthedocs.io/en/stable/
# Inspiration: https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html

# Bot Name: u/theLadled
def load_ladle()->praw.Reddit:
        reddit= praw.Reddit("LadleBot")
        return reddit

def load_posts(amount: int):
    if amount < 0 or amount > 100:
         amount = 25 # Default Cutoff
    reddit = load_ladle()

    sub_list = ["piano","guitar","classicalmusic","learnprogramming","computerscience","machinelearning","math"]

    search = ""
    for sub in sub_list[:-1]:
        search += sub + "+"
    search += sub_list[-1]

    posts = []
    for submission in reddit.subreddit(search).hot(limit=amount):
        info = f"{submission.title} {submission.upvote_ratio} {submission.url} {submission.score}"  
        posts.append((f"{submission.title}",submission.upvote_ratio,submission.score))
    
    posts = sorted(posts,key=lambda x : x[1] * x[2],reverse=True)

    return posts

def main():
    items = load_posts(30)
    for post in items:
         print(post)
     

if __name__ == "__main__":
    main()