from flask import Flask, make_response, redirect, session, flash, render_template, jsonify
from flask_restful import abort, Api, Resource

from loginform import LoginForm
from regform import RegForm
from db import db, Users
from config import HOST, PORT


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yandexlyceum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()
api = Api(app)


class Logout(Resource):

    def get(self):
        session.pop('username')
        session.pop('user_id')
        session.pop('status')
        return redirect('/login')


class Login(Resource):

    def __init__(self):
        super().__init__()
        self.form = LoginForm()

    def get(self):
        return make_response(render_template('login.html', titile='login', form=self.form))

    def post(self):
        if self.form.validate_on_submit():
            res = Users.query.filter_by(username=self.form.username.data).first()
            if res is not None:
                if res.check_password(self.form.password.data):
                    flash('ok', category='success')
                    return jsonify({'Авторизация': 'ok'})
                else:
                    flash('wrong password', category='danger')
            else:
                flash('user is not found', category='danger')
        return redirect('/login')


class Registration(Resource):

    def __init__(self):
        super().__init__()
        self.form = RegForm()

    def get(self):
        return make_response(render_template('registration.html', titile='registration', form=self.form))

    def post(self):
        if self.form.validate_on_submit():
            res = Users.query.filter_by(username=self.form.username.data).first()
            if res is None:
                if self.form.password_validate.data != self.form.password.data:
                    flash('Password validating failed', category='danger')
                    return redirect('/registration')
                user = Users(username=self.form.username.data, status='user', active=True,
                             name=self.form.name.data, surname=self.form.surname.data,
                             patronymic=self.form.patronymic.data)
                user.set_password(self.form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Successful!', category='success')
                return redirect('/login')
            flash('Account already exists', category='danger')
        return redirect('/registration')


api.add_resource(Registration, '/registration')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
