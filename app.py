from models import *
from flask import render_template, request, session
from forms import *
from passlib.hash import sha256_crypt


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errorpage.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    loginform = LoginForm()
    signupform = SignUpForm()

    if request.method == 'POST':
        if signupform.validate_on_submit() and signupform.signup.data:
            first_name = request.form['firstname']
            last_name = request.form['lastname']
            email = request.form['email']
            username = request.form['username']
            password = sha256_crypt.encrypt(str(request.form['password']))
            return render_template('display.html', data="{} : {} : {} : {} : {}".format(first_name, last_name, email, username, password), msg_suc="SignUp Successful")

        elif loginform.validate_on_submit() and loginform.login.data:
            username = request.form['username']
            password = request.form['password']
            return render_template('display.html', data="Hello {}".format(username), msg_suc="Login Successful")

        else:
            return render_template('index.html', loginform=loginform, signupform=signupform, msg_err="Please verify provided details.")

    elif request.method == 'GET':
        return render_template('index.html', loginform=loginform, signupform=signupform)


if __name__ == '__main__':
    app.run()
