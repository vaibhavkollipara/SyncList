from models import *
from flask import render_template, request, session, g, url_for, redirect
from forms import *
from functools import wraps
from passlib.hash import sha256_crypt


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpage.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') == None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user') != None:
        return redirect(url_for('dashboard'))
    loginform = LoginForm()
    signupform = SignUpForm()

    if request.method == 'POST':
        if signupform.validate_on_submit() and signupform.signup.data:
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            email = request.form['email']
            username = request.form['username']
            password = sha256_crypt.encrypt(str(request.form['password']))
            user = User(username=username, password_enc=password)
            user.details = UserDetails(first_name=first_name, last_name=last_name, email=email)
            db.session.add(user)
            db.session.commit()
            return render_template('display.html', data="{} : {} : {} : {} : {}".format(first_name, last_name, email, username, password), msg_suc="SignUp Successful")

        elif loginform.validate_on_submit() and loginform.login.data:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            if user == None:
                return render_template('index.html', loginform=loginform, signupform=signupform, msg_err="Please verify provided details.")
            if sha256_crypt.verify(password, user.password_enc):
                session['user'] = user.fullname
                session['uid'] = user.id
                return redirect(url_for('dashboard'))
            else:
                return render_template('index.html', loginform=loginform, signupform=signupform, msg_err="Invalid Credentails.Please try again.")

        else:
            return render_template('index.html', loginform=loginform, signupform=signupform, msg_err="Please verify provided details.")

    elif request.method == 'GET':
        return render_template('index.html', loginform=loginform, signupform=signupform)


@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['uid'])
    userslist = user.contactslist.all()
    return render_template('dashboard.html', userslist=userslist)


@app.route('/shared')
@login_required
def shared():
    user = User.query.get(session['uid'])
    userslist = user.sharedto.all()
    return render_template('shared.html', userslist=userslist)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
