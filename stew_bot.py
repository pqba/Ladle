import praw

# Inspiration: https://praw.readthedocs.io/en/latest/tutorials/reply_bot.html

# Bot Name: u/theLadled

with open("info.txt") as f:
    auth_info = []
    for line in f:
        auth_info.append(line)

    reddit = praw.Reddit(
        client_id =auth_info[0],
        client_secret =auth_info[1],
        password = auth_info[2],
        user_agent=auth_info[3],
        username=auth_info[4],
    )

print(reddit.user.me())

