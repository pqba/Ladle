import praw
from prawcore import NotFound
import nh3
import requests
import json


# Documentation: https://praw.readthedocs.io/en/stable/

# Inspiration: https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html

# Bot Name: u/theLadled
def load_ladle() -> praw.Reddit:
    return praw.Reddit("LadleBot")


def setup_ladle(client_id: str, client_secret: str, pw: str, u_agent: str, uname: str) -> praw.Reddit:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        password=pw,
        user_agent=u_agent,
        username=uname
    )
    return reddit


def info_load(amount=100, selected_subs=None) -> list:
    if selected_subs is None:
        selected_subs = ["popular"]
    if amount < 0 or amount > 100:
        amount = 50  # Default Cutoff
    reddit = load_ladle()

    search = ""
    for sub in selected_subs[:-1]:
        search += sub + "+"
    search += selected_subs[-1]

    post_ids = []
    for submission in reddit.subreddit(search).hot(limit=amount):
        post_ids.append(submission.fullname)  # Collect fullnames of the posts

    posts = []
    for submission in reddit.info(fullnames=post_ids):
        try:
            info = (f"r/{str(submission.subreddit.display_name).lower()}",
                    f"{submission.title}", int(float(submission.upvote_ratio) * 100), submission.score,
                    submission.url, submission.num_comments, submission.id)
            posts.append(info)
        except Exception as e:
            print(f"Error {e}")
    ordered = sort_posts(posts, True)
    return ordered


def load_posts(amount=100, selected_subs=None) -> list:
    if selected_subs is None:
        selected_subs = ["popular"]
    if amount < 0 or amount > 100:
        amount = 50  # Default Cutoff
    reddit = load_ladle()

    search = ""
    for sub in selected_subs[:-1]:
        search += sub + "+"
    search += selected_subs[-1]

    posts = []
    for submission in reddit.subreddit(search).hot(limit=amount):
        info = (f"r/{str(submission.subreddit).lower()}",
                f"{submission.title}", int(float(submission.upvote_ratio) * 100), submission.score,
                submission.url, submission.num_comments, submission.id)
        posts.append(info)

    ordered = sort_posts(posts, True)
    return ordered


def sort_posts(content: list, asc: bool) -> list:
    return sorted(content, key=lambda x: x[2] * x[3], reverse=asc)


def user_info(user_name: str) -> dict:
    user_name = user_name.lower()  # Reddit has lowercase user data
    if not user_exists(username=user_name):
        return None
    user_model = load_ladle().redditor(user_name)
    person_data = {
        'who': user_name,
        'id': user_model.id,
        'utc': user_model.created_utc,
        'c_karma': user_model.comment_karma,
        'l_karma': user_model.link_karma,
        'icon': user_model.icon_img
    }

    new_actions = user_model.new()  # Sublisting Generator
    rec_comments = []
    rec_posts = []
    for action in new_actions:
        if isinstance(action, praw.models.reddit.submission.Submission):
            rec_posts.append([action, action.score, action.num_comments, action.title])
        elif isinstance(action, praw.models.reddit.comment.Comment):
            rec_comments.append([action, action.body, action.score, action.link_id.replace("t3_", "")])
        else:
            continue  # Invalid action
    person_data['comments'] = rec_comments
    person_data['posts'] = rec_posts
    return person_data


def subreddit_info(sub_name: str) -> dict:
    sub_name = sub_name.lower()
    if not sub_exists(sub_name):
        return None

    sub_model = load_ladle().subreddit(sub_name)
    sub_data = {
        'id': sub_model.id,
        'name': sub_name,
        'desc': sub_model.public_description,
        'full_desc': sub_model.description,
        'utc': sub_model.created_utc,
        'subs': sub_model.subscribers,
        'nsfw': sub_model.over18
    }

    return sub_data


# Returns icon, banner, active users, and category of sub, empty if 429
def subreddit_about(sub_name: str):
    url = f"https://www.reddit.com/r/{sub_name}/about.json"
    req = requests.get(url)
    interpreted = json.loads(req.text)
    if 'error' in interpreted:  # For: {'message': 'Too Many Requests', 'error': 429}
        print(f"Subreddit {sub_name} about request error code:  {interpreted['error']}. Full Dict: {interpreted}")
        return {}
    parsed = interpreted["data"]
    # print(json.dumps(parsed, indent=4))
    sub_info = {
        'subtitle': parsed['title'],
        'header_title': parsed['header_title'],
        'active': parsed['accounts_active'],
        'category': parsed['advertiser_category'],
        'lang': parsed['lang'],
        # Icons/banners are in 2 different styles, removing possible '?' fixes image links.
        'icon': parsed['icon_img'].split("?")[0],
        'bannerA': parsed['banner_img'].split("?")[0],
        'bannerB': parsed['banner_background_image'].split("?")[0]
    }
    # Other interesting fields: submit_text, mobile_banner_image,
    # quarantine, and header_img
    return sub_info


# Searches subreddit for relevant posts on query in time frame, None if invalid name
def subreddit_search(sub_name: str, query: str, time: str) -> dict:
    if not sub_exists(sub_name):
        return None

    sub_model = load_ladle().subreddit(sub_name)
    search_data = {
        'sub': sub_name,
        'q': query
    }
    results = []
    for submission in sub_model.search(query, time_filter=time):  # Listing generator
        results.append([submission, submission.score, submission.num_comments, submission.title, submission.created_utc])
    search_data['results'] = results
    return search_data


def post_info(post_id: str) -> dict:
    if not post_exists(post_id):
        return None

    post_model = load_ladle().submission(post_id)

    post_data = {
        'id': post_id,
        'url': post_model.url,
        'title': post_model.title,
        'text': post_model.selftext,  # Markdown format
        'score': post_model.score,
        'ratio': int(float(post_model.upvote_ratio) * 100),
        'who': post_model.author.name,
        'by-icon': post_model.author.icon_img,
        'nsfw': post_model.over_18,
        'sub': post_model.subreddit,
        'utc': post_model.created_utc,
        'flair': post_model.link_flair_text,
        'lock': post_model.locked,
        'nc': post_model.num_comments
        # 'comments' : get_comment_list()
    }
    return post_data


# Mark string converted post as seen by hiding it
def mark_seen(post_id: str) -> None:
    if post_exists(post_id):
        post_model = load_ladle().submission(post_id)
        post_model.hide()


def mark_unseen(post_id: str) -> None:
    if post_exists(post_id):
        post_model = load_ladle().submission(post_id)
        post_model.unhide()


# FROM: https://www.reddit.com/r/redditdev/comments/68dhpm/praw_best_way_to_check_if_subreddit_exists_from/
def sub_exists(sub_name: str) -> bool:
    try:
        load_ladle().subreddits.search_by_name(sub_name, exact=True)
    except NotFound:
        return False
    return True


def user_exists(username: str) -> bool:
    username = username.lower()  # Lowercase search
    try:
        load_ladle().redditor(username).submissions
        load_ladle().redditor(username).id
    except NotFound:
        return False
    return True


def post_exists(post_id: str):
    try:
        load_ladle().submission(post_id).score
    except NotFound:
        return False
    return True


def clean(client_input: str) -> str:
    return nh3.clean(client_input)


def get_comment_list(post, lim=None):
    post.comments.replace_more(limit=lim)
    for comment in post.comments.list():
        print(comment.body)


def get_top_level_comments(post):
    post.comments.replace_more(limit=0)
    for top_level_comment in post.comments:
        print(str(top_level_comment.body).replace("\n", "|"))


# TODO: finish building comment tree using parent child relationship, allow for expansion as well
def build_comment_tree(comment: praw.models.comment_forest.CommentForest, depth: int):
    pass


def main():
    print(subreddit_search("python", "generator", "week"))


if __name__ == "__main__":
    main()
