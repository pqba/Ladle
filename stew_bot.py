import praw
from prawcore import NotFound
import nh3
import requests
import requests.auth
import configparser
import json


# Returns praw bot from praw.ini file
def load_ladle() -> praw.Reddit:
    return praw.Reddit("LadleBot")


# Returns praw bot from inputted strings
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

    combined_subs = ""
    for sub in selected_subs[:-1]:
        combined_subs += sub + "+"
    combined_subs += selected_subs[-1]

    posts = []
    for submission in reddit.subreddit(combined_subs).hot(limit=amount):
        info = (f"r/{str(submission.subreddit).lower()}",
                f"{submission.title}", int(float(submission.upvote_ratio) * 100), submission.score,
                submission.url, submission.num_comments, submission.id)
        posts.append(info)

    ordered = sort_posts(posts, True)
    return ordered


# Simple content sorting algorithm for display
def sort_posts(content: list, asc: bool, score_ind=2, ratio_ind=3) -> list:
    return sorted(content, key=lambda x: x[score_ind] * x[ratio_ind], reverse=asc)


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
def subreddit_about(sub_name: str) -> dict:
    api_handle = f"r/{sub_name}/about"
    interpreted = send_reddit_request(path=api_handle)
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
        'cm_icon': parsed['community_icon'].split("?")[0],
        'bannerA': parsed['banner_img'].split("?")[0],
        'bannerB': parsed['banner_background_image'].split("?")[0]
    }
    # Other interesting fields: submit_text, mobile_banner_image,
    # quarantine, and header_img
    return sub_info


# Searches subreddit for relevant posts on query in time frame, None if invalid name
def subreddit_search(sub_name: str, query: str, time: str) -> dict:
    if not sub_exists(sub_name) or not time_filter_exists(time) or query == "":
        return None
    sub_model = load_ladle().subreddit(sub_name)
    search_data = {
        'sub': sub_name,
        'q': query,
        'time': time
    }

    results = []
    for submission in sub_model.search(query, time_filter=time):  # Listing generator
        results.append([submission, submission.score, submission.num_comments, submission.title,
                        submission.created_utc, int(float(submission.upvote_ratio) * 100)])
    ordered_results = sort_posts(content=results, asc=True, score_ind=1, ratio_ind=5)
    search_data['results'] = ordered_results
    return search_data


def home_search(query: str, time: str) -> dict:
    if not time_filter_exists(time) or query == "":
        return None
    all_model = load_ladle().subreddit("all")
    search_data = {
        'q': query,
        'time': time
    }
    general_results = []
    for submission in all_model.search(query, time_filter=time):  # Listing generator
        general_results.append([str(submission), submission.score, submission.num_comments, submission.title,
                                submission.created_utc, f"r/{str(submission.subreddit)}",
                                int(float(submission.upvote_ratio) * 100)])

    ordered_content = sort_posts(content=general_results, asc=True, score_ind=1, ratio_ind=6)

    search_data['results'] = ordered_content

    return search_data


def post_info(post_id: str) -> dict:
    if not post_exists(post_id):
        return None

    post_model = load_ladle().submission(post_id)

    post_data = {
        'id': post_id,
        'url': post_model.url,
        'link': post_model.permalink,
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


# Mark string converted post id as seen by hiding it, does nothing if id invalid
def mark_seen(post_id: str) -> None:
    if post_exists(post_id):
        post_model = load_ladle().submission(post_id)
        post_model.hide()


# Unhides a given post from string id, does nothing if id invalid
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


def post_exists(post_id: str) -> bool:
    try:
        load_ladle().submission(post_id).score
    except NotFound:
        return False
    return True


def time_filter_exists(time_period: str) -> bool:
    return time_period in ["hour", "day", "week", "month", "year", "all"]


# Uses nh3 library to sanitize untrusted and rendered user input
def clean(client_input: str) -> str:
    return nh3.clean(client_input)


# Sends direct API request to Reddit from path given using praw.ini file for creds
def send_reddit_request(path: str) -> dict:
    config = configparser.ConfigParser()
    config.read('praw.ini')
    if 'LadleBot' not in config:
        print("You must configure a praw.ini file with a LadleBot to send a request!")
        return {'error': 'No praw.ini file'}
    client_id = config.get('LadleBot', 'client_id')
    client_secret = config.get('LadleBot', 'client_secret')
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    data = {
        'grant_type': 'password',
        'username': config.get('LadleBot', 'username'),
        'password': config.get('LadleBot', 'password')
    }
    headers = {'User-Agent': config.get('LadleBot', 'user_agent')}
    response = requests.post("https://www.reddit.com/api/v1/access_token", auth=auth, data=data, headers=headers)
    token = response.json()['access_token']
    # use token to make request
    headers = {**headers, **{'Authorization': f'bearer {token}'}}
    try:
        response = requests.get(f'https://oauth.reddit.com/{path}', headers=headers)
    except requests.exceptions.SSLError:
        return {'error': 'SSL Unexpected EOF for request'}
    # print(json.dumps(json.loads(response.text), indent=4))
    return json.loads(response.text)


# Uses streamable API[https://support.streamable.com/article/46-streamable-api] to get iframe for video
def send_streamable_request(video_id: str) -> dict:
    # Unsure of what ratelimit is, or of other aspects of API. Unclear documentation.
    url = f"https://api.streamable.com/videos/{video_id}"
    req_text = requests.get(url).text
    stream_info = json.loads(req_text)
    # print(json.dumps(stream_info,indent=4))
    return stream_info


# Fetches and finds maximum quality resolution for mpd video playlist, N/A if not found
def best_video_quality(mpd_url: str) -> str:
    # REFERENCES: https://www.reddit.com/r/redditdev/comments/nzq955/why_doesnt_vredditdashplaylistmpd_have_1080p_mp4s/
    #             https://www.cloudflare.com/learning/video/what-is-mpeg-dash/
    response = requests.get(mpd_url)
    if response.status_code == 200:
        page = response.content.decode('utf-8')  # Bytes to string
        max_quality = "N/A"
        for line in page.splitlines():
            cut_line = line.strip()
            if cut_line.startswith("<BaseURL") and "AUDIO" not in cut_line:
                height = cut_line.split('DASH_')[1].split(".mp4")[0]
                max_quality = f"{height}"
        return max_quality
    else:
        return "N/A"


# Returns list of the best quality image urls from submission.media_metadata
def gallery_links(media_data: dict) -> list[str]:
    image_package = []
    for img in media_data.values():
        largest_img_url = img['s']['u']
        image_package.append(largest_img_url)
    return image_package


def get_comments():
    pass


def build_comment_tree():
    pass


def main():
    res = home_search("steph", "month")



if __name__ == "__main__":
    main()
