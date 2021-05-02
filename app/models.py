from .import db,login_manager
from flask_login import current_user,UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime


class User (db.Model):
    __tablename__='users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email = db.Column(db.String(255), unique = True,nullable = False)
    bio = db.Column(db.String(255),default ='My Bio')
    profile_pic_path = db.Column(db.String(150),default ='default.png')
    hashed_password = db.Column(db.String(255),nullable = False)
    blog = db.relationship('Blog', backref='user', lazy='dynamic')
    comment = db.relationship('Comment', backref='user', lazy='dynamic')

    @property
    def set_password(self):
        raise AttributeError('You cannot read the password attribute')

    @set_password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.secure_password,password) 
    
    def save_u(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def __repr__(self):
        return f'User {self.username}'

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    content = db.Column(db.Text(), nullable = False)
    feature_image= db.Column(db.String,nullable=False)
    comment = db.relationship('Comment', backref='blog', lazy='dynamic')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def get_blog(id):
        blog = Blog.query.filter_by(id=id).first()

        return blog

    def __repr__(self):
        return f"Blog {self.title}"


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'), nullable=False)
    comment = db.Column(db.Text(),nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(id):
        comment = Comment.query.filter_by(id=id)
        return comment

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'comment: {self.comment}'


class Follower(db.Model):
    __tablename__ = 'followers'

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(255),unique=True, index=True)
    

    def save(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return f'Follower {self.email}'
        
class Quote:
    '''
    Blueprint class for quotes consumed from API
    '''
    def __init__(self, author, quote):
        self.author = author
        self.quote = quote
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)