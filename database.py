import sqlite3
from datetime import datetime, timezone

DATABASE_NAME = 'reddit_posts.db'

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        author_flair_text TEXT,
        title TEXT,
        description TEXT,
        url TEXT,
        created_utc INTEGER,
        contains_laptop BOOLEAN,
        is_selling BOOLEAN
    )
    ''')
    conn.commit()
    conn.close()

def save_post_to_db(post):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    
    # Check if the post already exists in the database
    cursor.execute("SELECT COUNT(*) FROM posts WHERE url = ?", (post['url'],))
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert the new post
        cursor.execute('''
        INSERT INTO posts (username, author_flair_text, title, description, url, created_utc, contains_laptop, is_selling)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (post['username'], post['author_flair_text'], post['title'], post['description'], post['url'], post['created_utc'], post['contains_laptop'], post['is_selling']))
    else:
        # Update the existing post
        cursor.execute('''
        UPDATE posts
        SET username = ?, author_flair_text = ?, title = ?, description = ?, created_utc = ?, contains_laptop = ?, is_selling = ?
        WHERE url = ?
        ''', (post['username'], post['author_flair_text'], post['title'], post['description'], post['created_utc'], post['contains_laptop'], post['is_selling'], post['url']))
    
    conn.commit()
    conn.close()

def get_latest_post_timestamp():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT MAX(created_utc) FROM posts')
    result = cursor.fetchone()[0]
    conn.close()
    
    if result is not None:
        return datetime.fromtimestamp(result)
    return None

def get_all_posts():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, author_flair_text, title, description, url, created_utc, contains_laptop, is_selling FROM posts')
    posts = cursor.fetchall()
    conn.close()

    return [
        {
            "username": username,
            "author_flair_text": author_flair_text,
            "title": title,
            "description": description,
            "url": url,
            "created_utc": datetime.fromtimestamp(created_utc, tz=timezone.utc).strftime('%d %b %Y, %I:%M %p')
        }
        for username, author_flair_text, title, description, url, created_utc, contains_laptop, is_selling in posts
    ]