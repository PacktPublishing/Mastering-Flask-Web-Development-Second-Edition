import logging
import random
from faker import Faker
from webapp import create_app
from webapp import db
from webapp.auth.models import User, Role
from webapp.blog.models import Post, Tag
from webapp.auth import bcrypt
from config import DevConfig


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

log = logging.getLogger(__name__)
app = create_app(DevConfig)
app.app_context().push()

faker = Faker()

fake_users = [
    {'username': 'user_default', 'role': 'default'},
    {'username': 'user_poster', 'role': 'poster'},
    {'username': 'admin', 'role': 'admin'}
]
fake_roles = ['default', 'poster', 'admin']


def generate_tags(n):
    tags = list()
    for i in range(n):
        tag_title = faker.color_name()
        tag = Tag.query.filter_by(title=tag_title).first()
        if tag:
            tags.append(tag)
            continue
        tag = Tag()
        tag.title = tag_title
        tags.append(tag)
        try:
            db.session.add(tag)
            db.session.commit()
        except Exception as e:
            log.error("Fail to add tag %s: %s" % (str(tag), e))
            db.session.rollback()
    return tags


def generate_roles():
    roles = list()
    for rolename in fake_roles:
        role = Role.query.filter_by(name=rolename).first()
        if role:
            roles.append(role)
            continue
        role = Role(rolename)
        roles.append(role)
        db.session.add(role)
        try:
            db.session.commit()
        except Exception as e:
            log.error("Erro inserting role: %s, %s" % (str(role),e))
            db.session.rollback()
    return roles

def generate_users():
    users = list()
    for item in fake_users:
        user = User.query.filter_by(username=item['username']).first()
        if user:
            users.append(user)
            continue
        user = User()
        poster = Role.query.filter_by(name=item['role']).one()
        user.roles.append(poster)
        user.username = item['username']
        user.password = bcrypt.generate_password_hash("password")
        users.append(user)
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            log.error("Eror inserting user: %s, %s" % (str(user), e))
            db.session.rollback()
    return users


def generate_posts(n, users, tags):
    for i in range(n):
        post = Post()
        post.title = faker.sentence()
        post.text = faker.text(max_nb_chars=1000)
        post.publish_date = faker.date_this_century(before_today=True, after_today=False)
        post.user_id = users[random.randrange(0, len(users))].id
        post.tags = [tags[random.randrange(0, len(tags))] for i in range(0, 2)]
        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
            log.error("Fail to add post %s: %s" % (str(post), e))
            db.session.rollback()

generate_roles()
generate_posts(100, generate_users(), generate_tags(5))
