import logging
import random
from faker import Faker
from webapp import create_app
from webapp.auth.models import User, Role
from webapp.blog.models import Post
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

tags = ['t1', 't2']


def generate_roles():
    roles = list()
    for rolename in fake_roles:
        role = Role.objects(name=rolename)
        if role:
            roles.append(role)
            continue
        role = Role(rolename)
        roles.append(role)
        try:
            role.save()
        except Exception as e:
            log.error("Erro inserting role: %s, %s" % (str(role),e))
    return roles


def generate_users():
    users = list()
    for item in fake_users:
        user = User.objects(username=item['username']).first()
        if user:
            users.append(user)
            continue
        user = User()
        role = Role.objects(name=item['role']).first()
        user.roles.append(role)
        user.username = item['username']
        user.password = bcrypt.generate_password_hash("password")
        users.append(user)
        try:
            user.save()
        except Exception as e:
            log.error("Eror inserting user: %s, %s" % (str(user), e))
    return users


def generate_posts(n, users, tags):
    for i in range(n):
        post = Post()
        post.title = faker.sentence()
        post.text = faker.text(max_nb_chars=1000)
        post.publish_date = faker.date_this_century(before_today=True, after_today=False)
        post.user = users[random.randrange(0, len(users))].id
        post.tags = [tags[random.randrange(0, len(tags))] for i in range(0, 2)]
        try:
            post.save()
        except Exception as e:
            log.error("Fail to add post %s: %s" % (str(post), e))

generate_roles()
generate_posts(100, generate_users(), tags)
