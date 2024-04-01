import praw

# Documentation: https://praw.readthedocs.io/en/stable/
# Inspiration: https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html

# Bot Name: u/theLadled
def load_ladle() -> praw.Reddit:
    reddit = praw.Reddit("LadleBot")
    return reddit

def load_posts(amount: int):
    if amount < 0 or amount > 100:
        amount = 25  # Default Cutoff
    reddit = load_ladle()

    sub_list = ["piano", "guitar", "classicalmusic", "learnprogramming", "computerscience", "machinelearning", "math"]

    search = ""
    for sub in sub_list[:-1]:
        search += sub + "+"
    search += sub_list[-1]

    posts = []
    for submission in reddit.subreddit(search).hot(limit=amount):
        info = (submission,f"{submission.title}",submission.upvote_ratio,submission.score,f"{submission.url}")
        posts.append(info)

    ordered = sort_posts(posts, True)

    return ordered

def sort_posts(content: list, inReverse: bool) -> list:
    return sorted(content, key=lambda x: x[2] * x[3], reverse=inReverse)

def relevant_info(content : list) -> list:
    display = []
    for item in content:
        relevant = item[1:] # Only the title, amount of upvotes, like ratio, and url
        display.append(relevant)
    return display

def main():
    items = load_posts(30)
    for post in items:
        print(post)


if __name__ == "__main__":
    main()
