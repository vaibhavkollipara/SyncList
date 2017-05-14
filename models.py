from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('appconfig.cfg')
app.config.from_pyfile('secretconfig.cfg')

db = SQLAlchemy(app)


contacts = db.Table('contacts',
                    db.Column('user_id', db.Integer, db.ForeignKey("User.id")),
                    db.Column('contact_id', db.Integer, db.ForeignKey("User.id"))
                    )

requests = db.Table('requests',
                    db.Column('to_id', db.Integer, db.ForeignKey("User.id")),
                    db.Column('from_id', db.Integer, db.ForeignKey("User.id"))
                    )


class User(db.Model):

  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(length=20), unique=True)
  password_enc = db.Column(db.String(255))
  details = db.relationship("UserDetails", uselist=False, backref="user")

  # Requests received
  requestlist = db.relationship('User',
                                secondary=requests,
                                primaryjoin=(requests.c.to_id == id),
                                secondaryjoin=(requests.c.from_id == id),
                                lazy='dynamic')

  # Requests sent
  requested = db.relationship('User',
                              secondary=requests,
                              primaryjoin=(requests.c.from_id == id),
                              secondaryjoin=(requests.c.to_id == id),
                              lazy='dynamic')

  contactslist = db.relationship('User',
                                 secondary=contacts,
                                 primaryjoin=(contacts.c.user_id == id),
                                 secondaryjoin=(contacts.c.contact_id == id),
                                 lazy='dynamic')

  sharedto = db.relationship('User',
                             secondary=contacts,
                             primaryjoin=(contacts.c.contact_id == id),
                             secondaryjoin=(contacts.c.user_id == id),
                             lazy='dynamic')

  def __repr__(self):
    return "User({})".format(self.username)

  @property
  def fullname(self):
    if self.details == None:
      return 'User Details Not Set'
    else:
      return "{} {}".format(self.details.first_name, self.details.last_name)


class UserDetails(db.Model):

  __tablename__ = 'UserDetails'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('User.id'))
  first_name = db.Column(db.String(20))
  last_name = db.Column(db.String(20))
  email = db.Column(db.String(30), unique=True)
  numbers = db.relationship("Number", backref="userdetails", lazy='dynamic')

  def __repr__(self):
    return "UserDetails({}, {}, {})".format(self.first_name, self.last_name, self.email)


class Number(db.Model):
  __tablename__ = 'Number'
  id = db.Column(db.Integer, primary_key=True)
  userId = db.Column(db.Integer, db.ForeignKey('UserDetails.id'))
  tag = db.Column(db.String(20))
  number = db.Column(db.String(22), unique=True)

  def __repr__(self):
    return "Number({}, {})".format(self.tag, self.number)
