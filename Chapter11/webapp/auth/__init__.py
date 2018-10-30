import functools
from flask import flash, redirect, url_for, session, abort
from flask_login import current_user
from flask_openid import OpenID
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
from flask_dance.consumer import oauth_authorized
from flask_login import LoginManager, login_user
from flask_bcrypt import Bcrypt
from flask_login import AnonymousUserMixin
from flask_jwt_extended import JWTManager


class BlogAnonymous(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'


bcrypt = Bcrypt()
oid = OpenID()
jwt = JWTManager()

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.session_protection = "strong"
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "info"
login_manager.anonymous_user = BlogAnonymous


def create_module(app, **kwargs):
    bcrypt.init_app(app)
    oid.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)

    twitter_blueprint = make_twitter_blueprint(
        api_key=app.config.get("TWITTER_API_KEY"),
        api_secret=app.config.get("TWITTER_API_SECRET"),
    )
    app.register_blueprint(twitter_blueprint, url_prefix="/auth/login")

    facebook_blueprint = make_facebook_blueprint(
        client_id=app.config.get("FACEBOOK_CLIENT_ID"),
        client_secret=app.config.get("FACEBOOK_CLIENT_SECRET"),
    )
    app.register_blueprint(facebook_blueprint, url_prefix="/auth/login")

    from .controllers import auth_blueprint
    app.register_blueprint(auth_blueprint)


def authenticate(username, password):
    from .models import User
    user = User.query.filter_by(username=username).first()
    if not user:
        return None
    # Do the passwords match
    if not user.check_password(password):
        return None
    return user


def identity(payload):
    return load_user(payload['identity'])


def has_role(name):
    def real_decorator(f):
        def wraps(*args, **kwargs):
            if current_user.has_role(name):
                return f(*args, **kwargs)
            else:
                abort(403)

        return functools.update_wrapper(wraps, f)

    return real_decorator


@login_manager.user_loader
def load_user(userid):
    from .models import User
    return User.query.get(userid)


@oid.after_login
def create_or_login(resp):
    from .models import db, User
    username = resp.fullname or resp.nickname or resp.email
    if not username:
        flash('Invalid login. Please try again.', 'danger')
        return redirect(url_for('auth.login'))
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    return redirect(url_for('main.index'))


@oauth_authorized.connect
def logged_in(blueprint, token):
    from .models import db, User
    if blueprint.name == 'twitter':
        username = session.get('twitter_oauth_token').get('screen_name')
    elif blueprint.name == 'facebook':
        resp = facebook.get("/me")
        username = resp.json()['name']
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User()
        user.username = username
        db.session.add(user)
        db.session.commit()
    login_user(user)
    flash("You have been logged in.", category="success")
