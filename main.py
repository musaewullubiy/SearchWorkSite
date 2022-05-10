from requests import post, get, put, delete
import calendar
from datetime import datetime

from flask import Flask, render_template, redirect, abort, request, url_for
from flask_login import LoginManager, logout_user, login_required, login_user, current_user
from flask_restful import Api

from data import users_resources
from data import vacancy_resources
from data import projects_resources
from data import appointment_recource

from forms.add_appointment import AddAppointmentForm
from forms.add_user_photo import AddPhotoForm
from forms.authorization import AuthorizationForm
from forms.register import RegisterForm
from forms.search import SearchForm
from forms.add_about import AddAboutForm
from forms.add_project import AddProjectForm
from forms.add_vacancy import VacancyForm

from data.users import User
from data.projects import Project
from data.vacancies import Vacancy
from data.appointments import Appointments

from data import db_session

PATH = 'http://127.0.0.1:5000'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api = Api(app)


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')


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

    api.add_resource(appointment_recource.AppointmentResource, "/api/appointment/<int:appointment_id>")
    api.add_resource(appointment_recource.AppointmentListResource, "/api/appointment")

    app.run()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        string = form.search_text.data
        return redirect(f'/search/{form.search_text.data}')
    return render_template('index.html', title="searchwork", form=form)


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
            vacancies = list(db_sess.query(Vacancy).filter(Vacancy.hr_manager == user_id))
            return render_template('hr_profile.html', user=user, vacancies=vacancies)
        elif user.user_type == 'Соискатель':
            projects = list(db_sess.query(Project).filter(Project.developer_id == user_id))
            return render_template('user_profile.html', user=user, projects=projects)
    return abort(404)


@app.route('/profile')
@login_required
def user_profile_page():
    return redirect(f"profile/{current_user.id}")


@app.route('/vacancy/<int:vacancy_id>')
def vacancy_page(vacancy_id):
    db_sess = db_session.create_session()
    vacancy = db_sess.query(Vacancy).filter(Vacancy.id == vacancy_id).first()
    if vacancy:
        return render_template('vacancy.html', vacancy=vacancy)
    return abort(404)


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


@app.route('/add-about', methods=['GET', 'POST'])
@login_required
def add_about_page():
    form = AddAboutForm()
    if form.validate_on_submit():
        user = get(PATH + f'/api/users/{current_user.id}').json()['user']
        user['about'] = form.text.data
        put(PATH + f'/api/users/{current_user.id}', json=user)
        return redirect(f'/profile/{current_user.id}')
    return render_template('add_about.html', form=form)


@app.route('/add-project', methods=['GET', 'POST'])
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


@app.route('/search/<string:search_text>', methods=['GET', 'POST'])
def search_page_2(search_text):
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.search_text.data}')
    results = set()
    db_sess = db_session.create_session()
    for i in search_text.split():
        data = set(db_sess.query(Vacancy).filter(Vacancy.tags.like(f'%{i.lower()}%')).all())
        results = results | data
    return render_template('search_page.html', search_text=search_text, results=results, form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_page_1():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(f'/search/{form.search_text.data}')
    return render_template('search_page.html', form=form)


@app.route('/add-appointment/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add_appointment(user_id):
    vacancy_id = request.args.get('vacancy_id')
    form = AddAppointmentForm()
    if form.validate_on_submit():
        if current_user.user_type == "HR-менеджер":
            hr_man = current_user.id
            finder = user_id
        else:
            hr_man = user_id
            finder = current_user.id
        post(PATH + "/api/appointment",
             json={"message": form.message.data,
                   "date": form.date.data.strftime("%Y-%m-%d"),
                   "time": form.time.data.strftime("%H:%M"),
                   "platform": form.platform.data,
                   "link": form.link.data,
                   "hr": hr_man,
                   "finder": finder,
                   "vacancy_id": vacancy_id})
        return redirect('/')
    return render_template('add_appointment.html', form=form)


def calc_calender(date):
    year = date.year
    year_info = dict()
    for month in range(1, 13):
        days = calendar.monthcalendar(year, month)
        if len(days) != 6:
            days.append([0 for _ in range(7)])
        month_addr = calendar.month_abbr[month]
        year_info[month_addr] = days
    return year_info


@app.route('/calendar')
@login_required
def calendar_page():
    date = datetime.today()
    this_month = calendar.month_abbr[date.month]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    session = db_session.create_session()
    if current_user.user_type == 'HR-менеджер':
        data = session.query(Appointments).filter(Appointments.hr == current_user.id, Appointments.status == 1).all()
    else:
        data = session.query(Appointments).filter(Appointments.finder == current_user.id).all()
    appointments_date = []
    for i in data:
        appointments_date.append((months[i.datetime.month - 1], i.datetime.day))
    return render_template('calendar.html', this_month=this_month, date=date, content=calc_calender(date),
                           appointments_date=appointments_date, data=data)


@app.route('/applications')
@login_required
def application_page():
    sess = db_session.create_session()
    if current_user.user_type == "HR-менеджер":
        applications = sess.query(Appointments).filter(Appointments.hr == current_user.id,
                                                       Appointments.status == 0).all()
    else:
        applications = sess.query(Appointments).filter(Appointments.finder == current_user.id,
                                                       Appointments.status == 0).all()

    return render_template('application_page.html', applications=applications)


@app.route('/application/apply/<int:app_id>')
@login_required
def application_apply_page(app_id):
    sess = db_session.create_session()
    application = sess.query(Appointments).filter(Appointments.id == app_id).first()
    application.status = 1
    sess.commit()
    return redirect('/applications')


@app.route('/application/cancel/<int:app_id>')
@login_required
def application_cancel_page(app_id):
    sess = db_session.create_session()
    application = sess.query(Appointments).filter(Appointments.id == app_id).first()
    sess.delete(application)
    sess.commit()
    return redirect('/applications')


@app.route('/profile/add-photo', methods=['GET', 'POST'])
@login_required
def add_profile_photo_page():
    form = AddPhotoForm()
    if form.validate_on_submit():
        sess = db_session.create_session()
        user = sess.query(User).get(current_user.id)
        photo = form.add_photo.data
        name = f"{user.id}.{photo.filename.split('.')[-1]}"
        path = url_for("static", filename=f"profile-img")[1:]
        photo.save(path + "/" + name)
        user.photo = name
        sess.commit()
        return redirect(f'/profile/{current_user.id}')
    return render_template('add_photo.html', form=form)


if __name__ == '__main__':
    main()
