import datetime
import logging
from flask import render_template
from flask_mail import Message
from .. import celery, mail
from .models import Reminder, Post

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)
logs = logging.getLogger(__name__)


@celery.task()
def log(msg):
    return msg


@celery.task()
def multiply(x, y):
    return x * y


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self, pk):
    logs.info("Remind worker %d" % pk)
    reminder = Reminder.query.get(pk)
    msg = Message(body="Text %s" % str(reminder.text),
                  recipients=[reminder.email],
                  subject="Your reminder")
    try:
        mail.send(msg)
        logs.info("Email sent to %s" % reminder.email)
        return
    except Exception as e:
        logs.error(e)
        self.retry(exc=e)


@celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def digest(self):
    # find the start and end of this week
    year, week = datetime.datetime.now().isocalendar()[0:2]
    date = datetime.date(year, 1, 1)
    if (date.weekday() > 3):
        date = date + datetime.timedelta(7 - date.weekday())
    else:
        date = date - datetime.timedelta(date.weekday())
    delta = datetime.timedelta(days=(week - 1) * 7)
    start, end = date + delta, date + delta + datetime.timedelta(days=6)

    posts = Post.query.filter(
        Post.publish_date >= start,
        Post.publish_date <= end
    ).all()

    if (len(posts) == 0):
        return

    msg = Message()
    msg.html = render_template("digest.html", posts=posts)
    msg.recipients = ['']

    msg.subject = "Weekly Digest"
    try:
        mail.send(msg)
        return
    except Exception as e:
        logs.error(e)
        self.retry(exc=e)


def on_reminder_save(mapper, connect, self):
    remind.apply_async(args=(self.id,), eta=self.date)
