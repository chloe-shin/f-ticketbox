from flask_login import UserMixin
from src import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False, unique=False)
    admin = db.Column(db.Boolean, default=False)
    # ## list of events connected by user_id. make relationship with users.
    # events= db.relationship('Event', backref='user', lazy=True)
    # ## list of ratings connected by user_id. make relationship with users.
    # ratings= db.relationship('Rating', backref='user', lazy=True)
    # ## list of orders connected by user_id. make relationship with users.
    # orders= db.relationship('Order', backref='user', lazy=True)
    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password )
    
    def check_user(self):
        return User.query.filter_by(email=self.email).first()
## select * from users join events on users.id = events.user_id;

# class Event(db.Model):
#     __tablename__='events'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     title = db.Column (db.String, nullable=False)
#     image = db.Column(db.String, nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     location = db.Column(db.String, nullable=False)
#     time = db.Column(db.DateTime)
#     created = db.Column(db.DateTime, server_default=db.func.now())

#     tickets = db.relationship('Ticket', backref='events', lazy=True)
#     ratings = db.relationship('Rating', backref='events', lazy=True)

# class Rating(db.Model):
#     __tablename__='ratings'
#     id = db.Column(db.Integer, primary_key=True)
#     star = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
#     event_id = db.Column(db.Integer,db.ForeignKey('events.id'), nullable=False, primary_key=True)

# class Order(db.Model):
#     __tablename__='orders'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

#     order_items = db.relationship('OrderItem', backref='order', lazy=True)

# class OrderItem(db.Model):
#     __tablename__='order_items'
#     id = db.Column(db.Integer, primary_key=True)
#     order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
#     ticket_id = db.Column(db.Integer, nullable=False)

#     tickets = db.relationship('Ticket', backref='orderitem', lazy=True) 

# class Ticket(db.Model):
#     __tablename__='tickets'
#     id = db.Column(db.Integer, primary_key=True)
#     event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
#     orderitem_id = db.Column(db.Integer, db.ForeignKey('orderitem.id'), nullable=False)
#     kind = db.Column (db.String, nullable=False)
#     price = db.Column (db.String, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)

