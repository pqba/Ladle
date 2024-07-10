import praw
from prawcore import NotFound
import nh3

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
        info = (submission, f"r/{str(submission.subreddit.display_name).lower()}", 
                f"{submission.title}", submission.upvote_ratio, submission.score,
                f"{submission.url}",submission.id)
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

def user_info(user_name:str):
    user_name = user_name.lower() # Reddit has lowercase user data
    if not user_exists(username=user_name):
        return None
    person_data = {}
    user_model = load_ladle().redditor(user_name)

    person_data['who'] = user_name
    person_data['id'] = user_model.id

    person_data['utc'] = user_model.created_utc
    person_data['c_karma'] = user_model.comment_karma
    person_data['l_karma'] = user_model.link_karma
    person_data['icon'] = user_model.icon_img

    # TODO: finish User content
    #recent_comments = user_model.comments.new(limit=5)
    #parsed_comments = [c.body for c in recent_comments]
    #recent_posts = user_model.posts.new(limit=5)
    #person_data['r_comment'] = parsed_comments
    # person_data['r_posts'] =  ???
    return person_data

def subreddit_info(sub_name:str):
    sub_name = sub_name.lower()
    if not sub_exists(sub_name):
        return None
    sub_data = {}
    sub_model = load_ladle().subreddit(sub_name)
    
    sub_data['id']   = sub_model.id
    sub_data['name'] = sub_name
    sub_data['desc'] = sub_model.public_description
    sub_data['utc']  = sub_model.created_utc
    sub_data['subs'] = sub_model.subscribers
    sub_data['safe'] = sub_model.over18
    return sub_data

def post_info(post_id:str):
   if not post_exists(post_id):
       return None
   post_data = {}
   post_model = load_ladle().submission(post_id)
    
    # Post info
   post_data['id']    = post_id
   post_data['url']   = post_model.url
   post_data['title'] = post_model.title
   post_data['text']  = post_model.selftext
    
    # Popularity
   post_data['score'] = post_model.score
   post_data['ratio'] = post_model.upvote_ratio
    
   # Author
   author = post_model.author
   post_data['who'] = author.name
   post_data['by-icon'] = author.icon_img

   # Metadata
   post_data['safe']    = post_model.over_18
   post_data['sub']     = post_model.subreddit
   post_data['utc']     = post_model.created_utc
   post_data['flair']   = post_model.link_flair_text
   post_data['locked']  = post_model.locked

   # Comments
   post_data['nc'] = post_model.num_comments
   #post_data['comments'] = get_comment_list()

   return post_data

# Mark string converted post as seen by hiding it
def mark_seen(post_id:str):
    if not post_exists(post_id):
        return
    post_model = load_ladle().submission(post_id)
    post_model.hide()

# FROM: https://www.reddit.com/r/redditdev/comments/68dhpm/praw_best_way_to_check_if_subreddit_exists_from/
def sub_exists(subname:str):
    try:
        load_ladle().subreddits.search_by_name(subname, exact=True)
    except NotFound:
        return False
    return True

def user_exists(username:str):
    username = username.lower() # Lowercase search
    try: 
        load_ladle().redditor(username).submissions
        load_ladle().redditor(username).id
    except NotFound: 
        return False
    return True

def post_exists(post_id:str):
    try:
        load_ladle().submission(post_id).score
    except NotFound:
        return False
    return True

def clean(client_input:str):
    return nh3.clean(client_input)

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
