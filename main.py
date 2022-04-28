import datetime

from flask import Flask, render_template, redirect
from flask_login import current_user
from forms.authorization import AuthorizationForm
from forms.register import RegisterForm
from data.users import User
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/members.db")
    app.run()


@app.route('/')
def index():
    return render_template('index.html', title="Searchwork")


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
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            about='~',
            age=form.age.data,
            modified_date=datetime.datetime.now()
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def authorization():
    form = AuthorizationForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            if user.check_password(form.password.data):
                return redirect("/")
            else:
                return render_template("authorization.html", title="Авторизация", message="Неверный пароль", form=form)
        else:
            return render_template("authorization.html", title="Авторизация", message="Пользователь не найден",
                                   form=form)
    return render_template("authorization.html", title="Авторизация", form=form)


@app.route('/profile/hr/<int:hr_id>')
def profile_hr(hr_id):
    return render_template('hr_profile.html')


@app.route('/profile/user/<int:user_id>')
def profile_user(user_id):
    return render_template('user_profile.html')


if __name__ == '__main__':
    main()
