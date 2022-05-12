from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from dateutil.parser import *


class Pitches(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer,primary_key = True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    description = db.Column(db.String(), index = True)
    title = db.Column(db.String())
    category = db.Column(db.String(255), nullable=False)
    comments = db.relationship('Comments',backref='pitch',lazy='dynamic')
    upvotes = db.relationship('Upvotes', backref = 'pitch', lazy = 'dynamic')
    downvotes = db.relationship('Downvotes', backref = 'pitch', lazy = 'dynamic')
    posted = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def get_pitches(cls, id):
        pitches = Pitches.query.order_by(pitch_id=id).desc().all()
        return pitches

    @classmethod
    def get_my_pitches (cls, id):
        myPitches = Pitches.query.filter_by(owner_id = id).all()
        return myPitches

    def __repr__(self):
        return f'Pitch {self.description}'

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    pass_secure = db.Column(db.String(255))
    my_pitch = db.relationship('Pitches', backref='user', lazy='dynamic')
    comment = db.relationship('Comments', backref = 'user', lazy = 'dynamic')
    upvotes = db.relationship('Upvotes', backref = 'user', lazy = 'dynamic')
    downvotes = db.relationship('Downvotes', backref = 'user', lazy = 'dynamic')

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

    

class Upvotes(db.Model):
    _tablename__ = 'upvotes'
    id = db.Column(db.Integer,primary_key=True)
    upvote = db.Column(db.Integer,default=1)
    pitch_u_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    def save_upvotes(self):
        db.session.add(self)
        db.session.commit()

    def add_upvotes(cls,id):
        upvote_pitch = Upvotes(user = current_user, pitch_u_id=id)
        upvote_pitch.save_upvotes()

    @classmethod
    def get_upvotes(cls,id):
        upvote = Upvotes.query.filter_by(pitch_u_id=id).all()
        return upvote

    @classmethod
    def get_all_upvotes(cls,pitch_id):
        upvotes = Upvotes.query.order_by('id').all()
        return upvotes

    @classmethod
    def check_user_voted(cls,user_u_id,pitch_v_id):
        chkupvote = Upvotes.query.filter_by(user_id= user_u_id, pitch_id= pitch_v_id)

    def __repr__(self):
        return f'{self.user_id}:{self.pitch_u_id}'
        
class Downvotes(db.Model):

    __tablename__ = 'downvotes'
    id = db.Column(db.Integer,primary_key=True)
    downvote = db.Column(db.Integer,default=1)
    pitch_d_id = db.Column(db.Integer,db.ForeignKey('pitches.id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    def save_downvotes(self):
        db.session.add(self)
        db.session.commit()
    def add_downvotes(cls,id):
        downvote_pitch = Downvotes(user = current_user, pitch_d_id=id)
        downvote_pitch.save_downvotes()
    @classmethod
    def get_downvotes(cls,id):
        downvote = Downvotes.query.filter_by(pitch_id=id).all()
        return downvote
    @classmethod
    def get_all_downvotes(cls,pitch_id):
        downvote = Downvotes.query.order_by('id').all()
        return downvote
    def __repr__(self):
        return f'{self.user_id}:{self.pitch_d_id}'

class Comments(db.Model):

    __tablename__='comments'
    id = db.Column(db.Integer,primary_key=True)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"Comment : id: {self.id} comment: {self.description}"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))