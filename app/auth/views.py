from flask import render_template, url_for, redirect, flash,request
from . import auth
from ..models import User
from .forms import Registration, LoginForm
from .. import db
from flask_login import logout_user, login_user, login_required,login_remembered
from ..email import mail_message
@auth.route('/login', methods=["GET","POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user is not None and user.verify_hash(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next')or url_for('main.index'))
        flash('Invalid username or password') 

    return render_template('authentic/login.html',login_form=login_form)

@auth.route('/register', methods=["GET","POST"])
def register():
    form = Registration()
    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)
        db.session.add(user)
        db.session.commit()
        mail_message("Welcome to watchlist","email/welcome_user",user.email,user=user)
        return redirect(url_for('auth.login'))
    return render_template('authentic/registration.html', form =form) 


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))   