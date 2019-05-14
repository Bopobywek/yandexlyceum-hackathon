from flask import Flask, make_response, redirect, session, flash, render_template, jsonify
from flask_restful import abort, Api, Resource, reqparse
from uuid import uuid4

from loginform import LoginForm
from regform import RegForm
from add_task_form import AddTaskForm
from db import db, Users, Tasks
from config import HOST, PORT


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yandexlyceum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
db.create_all()
api = Api(app)


def abort_if_user_status_bad_request(user_status):
    if user_status not in ['admin', 'user'] and user_status is not None:
        abort(400, message='user_status should be "admin" or "user"')


def generate_token():
    return uuid4()


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
                    session['username'] = res.username
                    session['user_id'] = res.id
                    session['status'] = res.status
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
        return make_response(render_template('registration.html', title='registration', form=self.form))

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


class AddTask(Resource):

    def __init__(self):
        super().__init__()
        self.form = AddTaskForm()

    def get(self):
        if session.get('username') is not None:
            return make_response(render_template('add-task.html', title='Add task', form=self.form))
        return redirect('/login')

    def post(self):
        if self.form.validate_on_submit():
            user = Users.query.filter_by(username=session.get('username')).first()
            t = Tasks(title=self.form.title.data, content=self.form.content.data, creator_id=user.id,
                      deadline=self.form.deadline.data)
            db.session.add(t)
            db.session.commit()
            return redirect('/')
        return redirect('/add-task')


class TasksResource(Resource):

    def get(self):
        tasks = Tasks.query.all()
        return make_response(render_template('tasks.html', tasks=tasks))


class AuthAPI(Resource):

    def post(self):
        parser = AuthParser()
        parser.post_parser()
        parser = parser.return_parser_object()
        args = parser.parse_args()
        if 'password' in args and 'login' in args:
            user = Users.query.filter_by(username=args['login']).first()
            token_generated = generate_token()
            user.token = token_generated
            db.session.commit()
            return jsonify({'status': 'OK', 'token': token_generated})
        else:
            return jsonify({'status': 'Bad Request'})


class AuthParser(object):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post_parser(self):
        self.parser.add_argument('login', required=True)
        self.parser.add_argument('password', required=True)

    def return_parser_object(self):
        return self.parser


api.add_resource(TasksResource, '/', '/tasks')
api.add_resource(AuthAPI, '/api/auth')
api.add_resource(AddTask, '/add-task')
api.add_resource(Registration, '/registration')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
