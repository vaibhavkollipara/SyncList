from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from validators import Unique
from models import User, UserDetails, Number


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username required")], render_kw={"placeholder": "username", "autofocus": "true"})
    password = PasswordField('Password', validators=[InputRequired(message="Password required")], render_kw={"placeholder": "password"})
    login = SubmitField('Login')


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(message="First Name Required"), Length(min=3, max=20, message="3 < no. of characters < 20")], render_kw={"placeholder": "First Name", "autofocus": "true"})
    lastname = StringField('Last Name', validators=[InputRequired(message="First Name Required"), Length(min=3, max=20, message="3 < no. of characters < 20")], render_kw={"placeholder": "Last Name"})
    email = StringField('Email', validators=[InputRequired(message="Email Required"), Email(),
                                             Unique(
        UserDetails,
        UserDetails.email,
        message='Email already Registered.'
    )
    ], render_kw={"placeholder": "email"})
    username = StringField('Username', validators=[InputRequired(message="Username required"), Length(min=3, max=20, message="3 < no. of characters < 20"),
                                                   Unique(
        User,
        User.username,
        message='Username already taken.')
    ], render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[InputRequired(message="Password required"), Length(min=6, max=20, message="6 < no. of characters < 20")], render_kw={"placeholder": "Password"})

    confirm = PasswordField('Cofirm Password', validators=[InputRequired(message="Confirm password required"), Length(min=6, max=20, message="6 < no. of characters < 20"), EqualTo('password', message="Passwords do not match")], render_kw={"placeholder": "Confirm Password"})
    signup = SubmitField('SignUp')


class RequestForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(message="please enter a username"), Length(min=3, max=20, message="3< no. of characters < 20")], render_kw={"placeholder": "username"})
    request = SubmitField('Request')


class PhoneForm(FlaskForm):
    tag = StringField('Tag', validators=[InputRequired(message="Tag required")], render_kw={"placeholder": "tag"})
    number = StringField('Tag', validators=[InputRequired(message="Number required"), Length(min=10, max=10, message="should have 10 digits only"),
                                            Unique(
        Number,
        Number.number,
        message='Number already Registered.'
    )
    ], render_kw={"placeholder": "number"})
    add = SubmitField('Add Number')
