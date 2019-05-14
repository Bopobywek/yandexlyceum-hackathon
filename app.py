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


@app.errorhandler(404)
def not_found(e):
    return abort(404, message='Task is not found')


def generate_token():
    return uuid4().hex


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
            if user is not None:
                if user.check_password(args['password']):
                    token_generated = generate_token()
                    user.token = token_generated
                    db.session.commit()
                    return jsonify({'status': 'OK', 'token': token_generated, 'code': '200'})
                else:
                    return abort(401, message='Wrong password')
            else:
                return abort(404, message='Wrong login')
        else:
            return abort(400, message='Bad Request')


class AuthParser(object):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post_parser(self):
        self.parser.add_argument('login', required=True)
        self.parser.add_argument('password', required=True)

    def return_parser_object(self):
        return self.parser


class TaskParser(object):

    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post_parser(self):
        self.parser.add_argument('token', required=True)

    def post_parser2(self):
        self.parser.add_argument('token', required=True)
        self.parser.add_argument('title', required=True)
        self.parser.add_argument('content', required=True)
        self.parser.add_argument('deadline', required=True)
        self.parser.add_argument('priority', required=True)

    def put_parser(self):
        self.parser.add_argument('token', required=True)
        self.parser.add_argument('title', required=False, default=None)
        self.parser.add_argument('content', required=False, default=None)
        self.parser.add_argument('deadline', required=False, default=None)
        self.parser.add_argument('priority', required=False, default=None)

    def return_parser_object(self):
        return self.parser


class TaskAPI(Resource):

    def get(self):
        parser = TaskParser()
        parser.post_parser()
        parser = parser.return_parser_object()
        args = parser.parse_args()
        if 'token' in args:
            res = Users.query.filter_by(token=args.get('token')).first()
            if res is not None:
                tasks = [el.get_info() for el in Tasks.query.filter_by(creator_id=res.id).all()]
                res = {'status': 'OK', 'task': tasks}
                return jsonify(res)
            else:
                return abort(403, message='Bad Token')
        else:
            return abort(400, message='Bad Request')

    def post(self):
        parser = TaskParser()
        parser.post_parser2()
        parser = parser.return_parser_object()
        args = parser.parse_args()
        if 'token' in args:
            res = Users.query.filter_by(token=args.get('token')).first()
            if res is not None:
                db.session.add(Tasks(title=args.get('title'), content=args.get('content'), creator_id=res.id,
                                     deadline=args.get('deadline'), priority=args.get('priority')))
                db.session.commit()
                return jsonify({'status': 'OK'})
            else:
                return abort(403, message='Bad Token')
        else:
            return abort(400, message='Bad Request')


class TaskIdAPI(Resource):
    
    def get(self, id):
        parser = TaskParser()
        parser.post_parser()
        parser = parser.return_parser_object()
        args = parser.parse_args()
        if 'token' in args:
            res = Users.query.filter_by(token=args.get('token')).first()
            if res is not None:
                task = Tasks.query.filter_by(id=id).first()
                if task is not None:
                    res = {'status': 'OK', 'tasks': task.get_info()}
                    return jsonify(res)
                else:
                    return abort(404, message='Task not found')
            else:
                return abort(403, message='Bad Token')
        else:
            return abort(400, message='Bad Request')
    
    def put(self, id):
        parser = TaskParser()
        parser.put_parser()
        parser = parser.return_parser_object()
        args = parser.parse_args()
        if 'token' in args:
            res = Users.query.filter_by(token=args.get('token')).first()
            if res is not None:
                task = Tasks.query.filter_by(id=id, creator_id=res.id).first()
                if task is not None:
                    task.title = args.get('title') if args.get('title') is not None else task.title
                    task.content = args.get('content') if args.get('content') is not None else task.content
                    task.priority = args.get('priority') if args.get('priority') is not None else task.priority
                    task.deadline = args.get('deadline') if args.get('deadline') is not None else task.deadline
                    res = {'status': 'OK'}
                    return jsonify(res)
                else:
                    return abort(404, message='Task not found')
            else:
                return abort(403, message='Bad Token')
        else:
            return abort(400, message='Bad Request')

    def delete(self, id):
        parser = TaskParser()
        parser.post_parser()
        parser = parser.return_parser_object()
        args = parser.parse_args()
        if 'token' in args:
            res = Users.query.filter_by(token=args.get('token')).first()
            if res is not None:
                task = Tasks.query.filter_by(id=id, creator_id=res.id).first()
                if task is not None:
                    db.session.delete(task)
                    db.session.commit()
                    return jsonify({'status': 'OK'})
                else:
                    abort(404, message='Task not Found')
            else:
                return abort(403, message='Invalid Login or Password')


api.add_resource(TasksResource, '/', '/tasks')
api.add_resource(TaskAPI, '/api/task')
api.add_resource(TaskIdAPI, '/api/task/<int:id>')
api.add_resource(AuthAPI, '/api/auth')
api.add_resource(AddTask, '/add-task')
api.add_resource(Registration, '/registration')
api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=True)
