from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from validators import Unique
from models import User, UserDetails


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username required")])
    password = PasswordField('Password', validators=[InputRequired(message="Password required")])
    login = SubmitField('Login')


class SignUpForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(message="First Name Required"), Length(min=3, max=20, message="3 < no. of charactes < 20")])
    lastname = StringField('Last Name', validators=[InputRequired(message="First Name Required"), Length(min=3, max=20, message="3 < no. of charactes < 20")])
    email = StringField('Email', validators=[InputRequired(message="Email Required"), Email(),
                                             Unique(
        UserDetails,
        UserDetails.email,
        message='Email already Registered.'
    )
    ])
    username = StringField('Username', validators=[InputRequired(message="Username required"), Length(min=3, max=20, message="3 < no. of charactes < 20"),
                                                   Unique(
        User,
        User.username,
        message='Username already taken.')
    ])
    password = PasswordField('Password', validators=[InputRequired(message="Password required"), Length(min=6, max=20, message="6 < no. of charactes < 20")])

    confirm = PasswordField('Cofirm Password', validators=[InputRequired(message="Confirm password required"), Length(min=6, max=20, message="6 < no. of charactes < 20"), EqualTo('password', message="Passwords do not match")])
    signup = SubmitField('SignUp')
