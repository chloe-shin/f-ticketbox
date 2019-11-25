
from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash
import requests 
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import User
from src import app, db
from itsdangerous import URLSafeTimedSerializer

root_blueprint = Blueprint('root', __name__, template_folder='../../templates')


def send_email(token, email, name):
        url= "https://api.mailgun.net/v3/sandbox4653e5e44b624763acb2fdd1c24c902c.mailgun.org/messages"
        try:
                response = requests.post(url, 
                           auth=("api", app.config['EMAIL_API']), 
                           data={"from": 'chloe <chloe.jihye@gmail.com>',
                           "to": [email], 
                           "subject": "Reset Password", 
                           "text":f"Hi {name} to reset password please check http://localhost:5000/user/new_password/{token}."}
                           )
                response.raise_for_status()
        except Exception as err:
                print(f'Other error occurred: {err}')  # Python 3.6
        else:
                print('Success!') 

#resetpassword
@root_blueprint.route('/resetpassword', methods=["GET","POST"])
def resetpassword():
        if current_user.is_authenticated:
                return redirect(url_for('root.home'))
        
        if request.method == "POST":
                user = User(email=request.form['email']).check_user()  
                if not user:
                        print("Account does not exsist")
                        return redirect(url_for('root.resetpassword'))
                s = URLSafeTimedSerializer(app.secret_key)
                token = s.dumps(user.email, salt="RESET_PASSWORD")
                send_email(token, user.email, user.name)
                print('OK')
                return redirect(url_for('root.login'))
                # s.loads(token, salt="RESET_PASSWORD", max_age=5)       
        return render_template("resetpassword.html")

#load homepage
@root_blueprint.route('/', methods=["GET"])
def home():
        # events = Event.query.order_by(Post.created.desc()).all()
        return render_template("home.html")

#login
@root_blueprint.route('/login', methods=["GET","POST"])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('root.home'))
        if request.method == 'POST':
            # logics
                user = User.query.filter_by(email=request.form['email']).first()
                if not user:
                        flash('Email is not registered', 'warning')
                        return redirect(url_for('root.register'))
                
                if user.check_password(request.form['password']):
                        login_user(user)
                        flash(f'Welcome back {current_user.name}', 'success')
                        return redirect(url_for('root.home'))
                flash('wrong password', 'warning')
                return redirect(url_for('root.login'))
        
        return render_template("login.html")
        
#register
@root_blueprint.route('/register', methods=["GET","POST"])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('root.home'))
        
        if request.method == 'POST':
                check_email = User.query.filter_by(email=request.form['email']).first()
                if check_email:
                        flash('email is already taken', 'warning')
                        return redirect(url_for('root.register'))
                new_user = User(email=request.form['email'], 
                                name=request.form['name'])
                new_user.set_password(request.form['password'])
                db.session.add(new_user)
                db.session.commit()
                login_user(current_user)
                flash('successfully create an account and logged in', 'success')
                return redirect(url_for('root.home'))
        
        return render_template("register.html")

#logout
@root_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('root.home'))


@root_blueprint.route('/newpassword/<token>', methods=["GET","POST"])
def newpassword():
        print(token)
        s = URLSafeTimedSerializer(app.secret_key)
        email = s.loads(token, salt="RESET_PASSWORD", max_age: 300)
        print(email)
        user= User(email = email().check_user)
        if not user:
                print('invalid token', 'token=token')
                return redirect(url_for('root.home'))
        if request.method == 'POST':
                if request.form[password] != request.form['confirm']:
                        print('root.bp~')
                        return redirect(url_for('root.home'))
                user.set_password(request.form['password'])
                 return redirect(url_for('root.home'))
        return render_template("newpassword.html")


