import datetime
from .. import db

tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    publish_date = db.Column(db.DateTime(), default=datetime.datetime.now)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))
    youtube_id = db.Column(db.String(255))
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return "<Post '{}'>".format(self.title)


class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text(), nullable=False)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)
    post_id = db.Column(db.Integer(), db.ForeignKey('post.id'))

    def __repr__(self):
        return "<Comment '{}'>".format(self.text[:15])


class Tag(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)

    def __init__(self, title=""):
        self.title = title

    def __repr__(self):
        return "<Tag '{}'>".format(self.title)


class Reminder(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    email = db.Column(db.String())
    text = db.Column(db.Text())

    def __repr__(self):
        return "<Reminder '{}'>".format(self.text[:20])
