from flask import (render_template,
                   Blueprint,
                   redirect,
                   url_for,
                   flash)
from flask_login import login_user, logout_user
from . import oid
from .models import mongo, User
from .forms import LoginForm, RegisterForm, OpenIDForm

auth_blueprint = Blueprint(
    'auth',
    __name__,
    template_folder='../templates/auth',
    url_prefix="/auth"
)


@auth_blueprint.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    form = LoginForm()
    openid_form = OpenIDForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        user = User.objects(username=form.username.data)[0]
        login_user(user, remember=form.remember.data)
        flash("You have been logged in.", category="success")
        return redirect(url_for('main.index'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")
    return render_template('login.html', form=form, openid_form=openid_form)


@auth_blueprint.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for('main.index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
@oid.loginhandler
def register():
    form = RegisterForm()
    openid_form = OpenIDForm()

    if openid_form.validate_on_submit():
        return oid.try_login(
            openid_form.openid.data,
            ask_for=['nickname', 'email'],
            ask_for_optional=['fullname']
        )

    if form.validate_on_submit():
        new_user = User(form.username.data)
        new_user.set_password(form.password.data)
        new_user.save()
        flash("Your user has been created, please login.", category="success")
        return redirect(url_for('.login'))

    openid_errors = oid.fetch_error()
    if openid_errors:
        flash(openid_errors, category="danger")
    return render_template('register.html', form=form, openid_form=openid_form)
