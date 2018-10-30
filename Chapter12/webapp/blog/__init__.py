from sqlalchemy import event
from .models import db, Reminder
from .tasks import on_reminder_save


def create_module(app, **kwargs):
    event.listen(Reminder, 'after_insert', on_reminder_save)
    from .controllers import blog_blueprint
    app.register_blueprint(blog_blueprint)
