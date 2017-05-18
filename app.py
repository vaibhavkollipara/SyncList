from models import *
from flask import render_template, request, session, g, url_for, redirect
from forms import *
from functools import wraps
from passlib.hash import sha256_crypt
from flask_wtf.csrf import CSRFProtect


csrf = CSRFProtect(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpage.html')


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


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
            return render_template('index.html', loginform=loginform, signupform=signupform, msg_suc="SignUp Successful.")

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
    if request.args.get('msg_suc'):
        return render_template('dashboard.html', userslist=userslist, msg_suc=request.args.get('msg_suc'))
    elif request.args.get('msg_info'):
        return render_template('dashboard.html', userslist=userslist, msg_info=request.args.get('msg_info'))
    elif request.args.get('msg_err'):
        return render_template('dashboard.html', userslist=userslist, msg_err=request.args.get('msg_err'))
    else:
        return render_template('dashboard.html', userslist=userslist)


@app.route('/request', methods=['GET', 'POST'])
@login_required
def requests():

    requestform = RequestForm()
    user = User.query.get(session['uid'])
    userslist = user.requested.all()

    if request.method == 'GET':
        return render_template('request.html', userslist=userslist, requestform=requestform)

    elif request.method == 'POST':

        if request.form.get('cancle') != None:
            req_user = User.query.get(int(request.form.get('uid')))
            user.requested.remove(req_user)
            db.session.commit()
            userslist.remove(req_user)
            return render_template('request.html', requestform=requestform, userslist=userslist, msg_suc="Request to {} cancelled".format(req_user.fullname))

        elif requestform.validate_on_submit() and requestform.request.data:
            username = str(request.form['username'])
            request_user = User.query.filter_by(username=username).first()
            if request_user is None:
                return render_template('request.html', requestform=requestform, userslist=userslist, msg_err="User with username <strong>{}</strong> does not exists.".format(username))
            elif request_user in user.contactslist.all():
                return render_template('request.html', requestform=requestform, userslist=userslist, msg_info="<strong>{}</strong> is already in your contacts".format(request_user.fullname))

            elif request_user in user.requested.all():
                return render_template('request.html', requestform=requestform, userslist=userslist, msg_info="Request already sent to <strong>{}</strong>".format(request_user.fullname))
            else:
                user.requested.append(request_user)
                db.session.commit()
                userslist.append(request_user)
                return render_template('request.html', requestform=requestform, userslist=userslist, msg_suc="Request sent to <strong>{}<strong>".format(request_user.fullname))
        else:
            return render_template('request.html', userslist=userslist, requestform=requestform)


@app.route('/pending', methods=['GET', 'POST'])
@login_required
def pending():
    user = User.query.get(session['uid'])
    userslist = user.requestlist.all()

    if request.method == 'GET':
        return render_template('pending.html', userslist=userslist)

    if request.method == 'POST':
        req_user = User.query.get(int(request.form.get('uid')))
        if request.form.get('ignore') != None:
            user.requestlist.remove(req_user)
            db.session.commit()
            userslist.remove(req_user)
            return render_template('pending.html', userslist=userslist, msg_suc="Request from {} deleted".format(req_user.fullname))
        elif request.form.get('accept') != None:
            user.contactslist.append(req_user)
            req_user.contactslist.append(user)
            user.requestlist.remove(req_user)
            if req_user in user.requested.all():
                user.requested.remove(req_user)
            db.session.commit()
            userslist.remove(req_user)
            return render_template('pending.html', userslist=userslist, msg_suc="Approved {}'s Request".format(req_user.fullname))


@app.route('/user', methods=["POST"])
@login_required
def userdetails():
    user = User.query.get(session['uid'])
    if request.form.get('uid') != None:
        req_user = User.query.get(int(request.form.get('uid')))
        if req_user == None:
            return render_template('user.html', msg_err="Invalid user details requested")
        elif req_user not in user.contactslist.all():
            return render_template('unauthorized.html')
        else:
            return render_template('user.html', user=req_user)

    elif request.form.get('deletecontact') != None:
        req_user = User.query.get(int(request.form.get('did')))
        user.contactslist.remove(req_user)
        req_user.contactslist.remove(user)
        db.session.commit()
        return redirect(url_for('dashboard', msg_suc="{} removed from your contacts.".format(req_user.fullname)))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    phoneform = PhoneForm()
    user = User.query.get(session['uid'])

    if request.method == "GET":
        return render_template('profile.html', user=user, phoneform=phoneform)

    elif request.method == "POST":
        if request.form.get('numdelete') != None:
            num = Number.query.get(int(request.form.get('nid')))
            db.session.delete(num)
            db.session.commit()
            return render_template('profile.html', user=user, phoneform=phoneform, msg_suc="Number Deleted")
        elif phoneform.validate_on_submit() and phoneform.add.data:
            tag = str(request.form.get('tag'))
            number = str(request.form.get('number'))
            user.details.numbers.append(Number(tag=tag, number=number))
            db.session.commit()
            return render_template('profile.html', user=user, phoneform=phoneform, msg_suc="New Number Added")
        else:
            return render_template('profile.html', user=user, phoneform=phoneform, msg_err="Problem Adding New Number")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
