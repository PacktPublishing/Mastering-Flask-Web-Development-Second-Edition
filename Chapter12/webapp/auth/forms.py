from flask_wtf import FlaskForm as Form
from flask_wtf import RecaptchaField
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, URL
from .models import User
from . import authenticate


class LoginForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        check_validate = super(LoginForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        if not authenticate(self.username.data, self.password.data):
            self.username.errors.append('Invalid username or password')
            return False
        return True


class OpenIDForm(Form):
    openid = StringField('OpenID URL', [DataRequired(), URL()])


class RegisterForm(Form):
    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=8)])
    confirm = PasswordField('Confirm Password', [
        DataRequired(),
        EqualTo('password')
    ])
    recaptcha = RecaptchaField()

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # if our validators do not pass
        if not check_validate:
            return False

        user = User.query.filter_by(username=self.username.data).first()

        # Is the username already being used
        if user:
            self.username.errors.append("User with that name already exists")
            return False

        return True
