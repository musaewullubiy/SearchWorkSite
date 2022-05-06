from flask import Flask, render_template, redirect
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from flask_restful import Api
from requests import post, get, put, delete

from data import users_resources
from data import vacancy_resources
from data import projects_resources
from forms.add_appointment import AddAppointmentForm

from forms.authorization import AuthorizationForm
from forms.register import RegisterForm
from forms.add_about import AddAboutForm
from forms.add_project import AddProjectForm
from forms.add_vacancy import VacancyForm
from forms.poisk_form import PoiskForm

from data.users import User
from data.projects import Project
from data.vacancies import Vacancy

from data import db_session

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

    api.add_resource(users_resources.UsersListResource, '/api/users')
    api.add_resource(users_resources.UsersResource, '/api/users/<int:user_id>')

    api.add_resource(vacancy_resources.VacancyResource, "/api/vacancy/<int:vacancy_id>")
    api.add_resource(vacancy_resources.VacancyListResource, "/api/vacancy")

    api.add_resource(projects_resources.ProjectResource, "/api/project/<int:project_id>")
    api.add_resource(projects_resources.ProjectListResource, "/api/project")

    app.run()


@app.route('/')
def index():
    poisk_form = PoiskForm()
    return render_template('index.html', title="searchwork", poisk_form=poisk_form)


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
@login_required
def profile_page(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if user:
        if user.user_type == 'HR-менеджер':
            return render_template('hr_profile.html', user=user)
        elif user.user_type == 'Соискатель':
            projects = db_sess.query(Project).filter(Project.developer_id == user_id)
            return render_template('user_profile.html', user=user, projects=projects)
    return '404'


@app.route('/add-vacancy', methods=["GET", "POST"])
@login_required
def add_vacancy():
    form = VacancyForm()
    if form.validate_on_submit():
        post(PATH + "/api/vacancy",
             json={"title": form.title.data,
                   "tags": form.tags.data.lower(),
                   "text": form.text.data,
                   "salary": form.salary.data,
                   "is_actual": form.is_actual.data,
                   "hr_manager": current_user.id})

        return redirect("/")
    return render_template("add_vacancy.html", title="Adding a vacancy", form=form)


@app.route('/add/about', methods=['GET', 'POST'])
@login_required
def add_about_page():
    form = AddAboutForm()
    if form.validate_on_submit():
        user = get(f'http://localhost:5000/api/users/{current_user.id}').json()['user']
        user['about'] = form.text.data
        put(f'http://localhost:5000/api/users/{current_user.id}', json=user)
        return redirect(f'/profile/{current_user.id}')
    return render_template('add_about.html', form=form)


@app.route('/add/project', methods=['GET', 'POST'])
@login_required
def add_project_page():
    form = AddProjectForm()
    if form.validate_on_submit():
        post(PATH + "/api/project",
             json={"title": form.title.data,
                   "link": form.link.data,
                   "developer_id": current_user.id})

        return redirect(f'/profile/{current_user.id}')
    return render_template('add_project.html', form=form)


@app.route('/delete-project/<int:project_id>')
@login_required
def delete_project(project_id):
    data = get(PATH + f'/api/project/{project_id}').json()['Project']
    try:
        if current_user.id == data['developer_id']:
            delete(PATH + f'/api/project/{project_id}')
            return redirect(f'/profile/{current_user.id}')
    except Exception:
        return redirect(f'/profile/{current_user.id}')
    return redirect(f'/profile/{current_user.id}')


@app.route('/search/<string:search_text>')
def search_page(search_text):
    results = set()
    db_sess = db_session.create_session()
    for i in search_text.split():
        data = set(db_sess.query(Vacancy).filter(Vacancy.tags.like(f'%{i.lower()}%')).all())
        results = results | data
    return render_template('search_page.html', results=results)


@app.route('/add-project/<int:user_id>')
def add_appointment(user_id):
    form = AddAppointmentForm()
    return render_template('add_appointment.html', form=form)


if __name__ == '__main__':
    main()
