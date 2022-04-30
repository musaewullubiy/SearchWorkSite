import datetime

from flask import Flask, render_template, redirect
from flask_login import current_user
from data import users_resources
from forms.authorization import AuthorizationForm
from forms.register import RegisterForm
from data.users import User
from data import db_session
from flask_login import LoginManager, logout_user, login_required, login_user

from flask_restful import Api

from requests import post


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


def main():
    db_session.global_init("db/members.db")

    api.add_resource(users_resources.UsersListResource, '/api/users')  # для списка объектов
    api.add_resource(users_resources.UsersResource,
                     '/api/users/<int:user_id>')  # для одного объекта

    app.run()


@app.route('/')
def index():
    return render_template('index.html', title="searchwork")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        print(post('http://localhost:5000/api/users', json={'name': form.name.data,
                                                               'surname': form.surname.data,
                                                               'about': '~',
                                                               'age': 17,
                                                               'email': form.email.data,
                                                               'hashed_password': form.password.data,
                                                               'user_type': form.user_type.data}).json())
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthorizationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('authorization.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('authorization.html', title='Авторизация', form=form)


@app.route('/profile/hr/<int:hr_id>')
def profile_hr(hr_id):
    return render_template('hr_profile.html')


@app.route('/profile/user/<int:user_id>')
def profile_user(user_id):
    return render_template('user_profile.html')


if __name__ == '__main__':
    main()
