#encoding: utf-8

from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100),nullable=False)


class Question(db.Model):
    __tablename__='question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #now() gets the time that the server runs for the first time
    #now gets the time that when the comment is posted.
    create_time = db.Column(db.DateTime, default=datetime.now)
    #foreign key
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    author = db.relationship('User', backref=db.backref('question'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    #create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question = db.relationship('Question', backref=db.backref('comments',order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('comments'))
