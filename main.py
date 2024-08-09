import praw
import json
import os
from datetime import datetime, timedelta, timezone
from llm_post_screening import check_post_with_llm
from database import init_db, save_post_to_db, get_latest_post_timestamp
import dotenv

dotenv.load_dotenv()

# REDDIT 
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
USER_AGENT = os.getenv('USER_AGENT')

# Configuration variables
SUBREDDIT = 'hardwareswap'
CHECK_INTERVAL = 60 * 24  # 24 hours
TIME_LIMIT = timedelta(hours=48)  # Check posts from the last 24 hours

# LLM prompt
LLM_PROMPT = """
Analyze the following Reddit post and determine if it contains a laptop for sale.
understand post properly and determine if the post author really mean a laptop in the post, this is a hardwareswap post from reddit so there will be GPUS, monitors and etc.
Return a JSON object with the following keys:
- "reasoning": a string explaining why the post is or is not about selling a laptop
- "contains_laptop": a boolean value indicating if the post is about selling a laptop
- "is_selling": a boolean value indicating if the post is about selling something
Title: {title}
Description: {description}
URL: {url}
"""

def fetch_new_reddit_posts(reddit, subreddit_name, time_limit):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    
    for post in subreddit.new(limit=None):
        post_time = datetime.fromtimestamp(post.created_utc)
        if post_time <= datetime.now() - time_limit:
            break
        
        if post.link_flair_text.lower() == 'buying':
            continue

        posts.append({
            'username': post.author.name,
            'author_flair_text': post.author_flair_richtext[0]['t'] if post.author_flair_richtext else None,
            'title': post.title,
            'description': post.selftext,
            'url': post.url,
            'created_utc': post.created_utc
        })
    
    return posts

def process_posts(posts):
    results = []
    for post in posts:
        llm_result = check_post_with_llm(LLM_PROMPT.format(**post))
        llm_data = json.loads(llm_result)
        print(llm_data["contains_laptop"])
        print(llm_data["reasoning"])
        print("")
        post['contains_laptop'] = llm_data['contains_laptop']
        post['is_selling'] = llm_data['is_selling']
        if post['contains_laptop'] and post['is_selling']:
            save_post_to_db(post)
            results.append(post)
    return results

def run_check(time_limit):
    reddit = praw.Reddit(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         user_agent=USER_AGENT)
    
    last_check_time = get_latest_post_timestamp()
    if last_check_time is None:
        last_check_time = datetime.now(timezone.utc) - time_limit

    posts = fetch_new_reddit_posts(reddit, SUBREDDIT, time_limit)
    if posts:
        process_posts(posts)
        print(f"Checked {len(posts)} new posts at {datetime.now()}")
    else:
        print(f"No new posts to check at {datetime.now()}")

def main():
    init_db()
    run_check(TIME_LIMIT)

if __name__ == "__main__":
    main()