from flask import Blueprint, session, redirect, url_for

babel_blueprint = Blueprint(
    'babel',
    __name__,
    url_prefix="/babel"
)


@babel_blueprint.route('/<string:locale>')
def index(locale):
    session['locale'] = locale
    return redirect(url_for('blog.home'))
