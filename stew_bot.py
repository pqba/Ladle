import praw


# Documentation: https://praw.readthedocs.io/en/stable/
# Inspiration: https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html

# Bot Name: u/theLadled
def load_ladle() -> praw.Reddit:
    reddit = praw.Reddit("LadleBot")
    return reddit


def setup_ladle(client_id: str, client_secret: str, pw: str, u_agent: str, uname: str) -> praw.Reddit:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=pw,
        user_agent=u_agent,
        username=uname
    )
    return reddit


def load_posts(amount: int, selected_subs=[]):
    if selected_subs is None:
        selected_subs = []
    if amount < 0 or amount > 100:
        amount = 25  # Default Cutoff
    reddit = load_ladle()

    sub_list = selected_subs

    search = ""
    for sub in sub_list[:-1]:
        search += sub + "+"
    search += sub_list[-1]

    posts = []
    for submission in reddit.subreddit(search).hot(limit=amount):
        info = (submission, f"r/{str(submission.subreddit.display_name).lower()}", f"{submission.title}",
                submission.upvote_ratio, submission.score, f"{submission.url}")
        posts.append(info)

    ordered = sort_posts(posts, True)
    return ordered


def sort_posts(content: list, inReverse: bool) -> list:
    return sorted(content, key=lambda x: x[3] * x[4], reverse=inReverse)


def relevant_info(content: list) -> list:
    display = []
    for item in content:
        relevant = item[1:]  # Only the title, amount of upvotes, like ratio, and url
        display.append(relevant)
    return display


def get_comment_list(post):
    post.comments.replace_more(limit=None)
    for comment in post.comments.list():
        print(comment.body)


def get_top_level_comments(post):
    post.comments.replace_more(limit=0)
    for top_level_comment in post.comments:
        print(str(top_level_comment.body).replace("\n", "|"))


# TODO: finish building comment tree using parent child relationship, allow for expansion as well
def build_comment_tree(post):
    pass


def main():
    items = load_posts(2)
    for post in items:
        get_top_level_comments(post[0])


if __name__ == "__main__":
    main()
