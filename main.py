import datetime

from flask import Flask, render_template, redirect
from flask_login import current_user
from data import users_resources
from data import vacancy_resoursers

from forms.authorization import AuthorizationForm
from forms.register import RegisterForm
from forms.add_about import AddAboutForm

from data.users import User
from data import db_session
from flask_login import LoginManager, logout_user, login_required, login_user

from flask_restful import Api

from requests import post, get, put

from forms.vacancy import VacancyForm

PATH = 'http://localhost:5000'


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
    api.add_resource(vacancy_resoursers.VacancyResource, "/api/vacancy/<int:vacancy_id>")
    api.add_resource(vacancy_resoursers.VacancyListResource, "/api/vacancy")

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
        post(PATH + '/api/users', json={'name': form.name.data,
                                        'surname': form.surname.data,
                                        'about': '~',
                                        'age': form.age.data,
                                        'email': form.email.data,
                                        'hashed_password': form.password.data,
                                        'user_type': form.user_type.data}).json()
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


@app.route('/profile/<int:user_id>')
def profile_page(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user:
        if user.user_type == 'HR-менеджер':
            return render_template('hr_profile.html', user=user)
        elif user.user_type == 'Соискатель':
            return render_template('user_profile.html', user=user)
    return '404'


@app.route('/addvacancy', methods=["GET", "POST"])
@login_required
def add_vacancy():
    add_form = VacancyForm()
    if add_form.validate_on_submit():
        post(PATH + "/api/vacancy",
             json={"tags": add_form.tags.data,
                   "text": add_form.text.data,
                   "salary": add_form.salary.data,
                   "is_actual": add_form.is_actual.data,
                   "hr_manager": current_user.id})

        return redirect("/")
    return render_template("addvacancy.html", title="Adding a vacancy", form=add_form)


@app.route('/add/about', methods=['GET', 'POST'])
def add_about_page():
    form = AddAboutForm()
    if form.validate_on_submit():
        user = get(f'http://localhost:5000/api/users/{current_user.id}').json()['user']
        user['about'] = form.text.data
        put(f'http://localhost:5000/api/users/{current_user.id}', json=user)
        return redirect(f'/profile/{current_user.id}')
    return render_template('add_about.html', form=form)


if __name__ == '__main__':
    main()
