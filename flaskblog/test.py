from operator import pos
from . import db
from .models import User, Post
from dateutil import parser

import sqlite3

conn = sqlite3.connect('flaskblog/temp.db')
cur = conn.cursor()

def copy_posts():
    user = User.query.get(1)
    cur.execute("SELECT * FROM post WHERE True")
    posts = cur.fetchall()
    for post in posts:
        date = parser.parse(post[2])
        new_post = Post(author=user, title=post[1], date_posted=date, content=post[3])
        db.session.add(new_post)
        db.session.commit()
    
copy_posts()

# from flaskblog import test