from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

users_identifier = db.Table('users_identifier', db.Model.metadata,
                            db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                            db.Column('task_id', db.Integer, db.ForeignKey('tasks.id')))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), unique=False, default='None')
    name = db.Column(db.String(80), unique=False, nullable=False)
    surname = db.Column(db.String(80), unique=False, nullable=False)
    patronymic = db.Column(db.String(80), unique=False, nullable=False)
    token = db.Column(db.String(80), unique=False, nullable=True)
    status = db.Column(db.String(10), unique=False, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Users {} {} {} {}>'.format(
            self.id, self.username, self.name, self.surname)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(1000), unique=True, nullable=False)
    category = db.Column(db.String(80), unique=True, nullable=False)
    deadline = ''
    stage = db.Column(db.String(80), unique=True, nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=False)
    creator = db.relationship('Users',
                              backref=db.backref('Tasks',
                                                 lazy=True))
    users = db.relationship("Users", secondary=users_identifier)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow())


if __name__ == '__main__':
    pass
