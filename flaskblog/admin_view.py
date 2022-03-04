from flask_admin.contrib.sqla import ModelView
from flaskblog import db, admin, bcrypt
from flask import url_for, redirect, request, abort
from flaskblog.models import User, Post
from flask_login import current_user
from flask_admin.contrib.fileadmin import FileAdmin
import os.path as op

def createsuperuser():
    username = input("Enter username: ")
    email = input("Enter Email adress: ")
    password = input("Enter Password: ")
    password2 = input("Enter Password again: ")
    if password == password2:
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password, is_admin=True)
        db.session.add(user)
        db.session.commit()
    else:
        print("passwords didn't match")

class Permission:
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class MicroBlogModelView(Permission, ModelView):
    pass


class MyFileAdmin(Permission, FileAdmin):
    pass

admin.add_view(MicroBlogModelView(User, db.session))
admin.add_view(MicroBlogModelView(Post, db.session))


path = op.join(op.dirname(__file__), 'static')
admin.add_view(MyFileAdmin(path, '/static/', name='Static Files'))