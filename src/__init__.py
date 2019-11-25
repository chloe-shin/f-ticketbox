from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, static_folder = "static")
app.config.from_object('config.Config')

db = SQLAlchemy(app)
from src.models import User

migrate = Migrate(app, db)
# for flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# flask_login > login_manager 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

from src.components.root import root_blueprint
app.register_blueprint(root_blueprint, url_prefix='/')

# from src.models.admin import MyAdmin
# admin = Admin(app, name='Chloe', template_mode='bootstrap3')
# admin.add_view(MyAdmin(User, db.session))