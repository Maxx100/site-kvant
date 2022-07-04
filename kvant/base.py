import os
import jinja2
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import PasswordField, BooleanField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from werkzeug.security import generate_password_hash
from data import db_session
from data.users import User, RegisterForm
from flask import Flask, render_template, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_code'

ip_config = {"ip": "127.0.0.1",
             "port": 8080}

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


class LoginForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            cookie_saver(user.email, user.hashed_password)
            return redirect("/kvant")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


def cookie_saver(email, password):
    res = make_response()
    res.set_cookie(email, password)
    return res


@app.route("/favicon.ico")
def favicon():
    return redirect("/static/favicon.ico")


@app.route("/<name>", methods=['GET', 'POST'])
def index(name):
    pics = []
    for i in os.listdir("static/img/pics/photos/"):
        pics.append("/static/img/pics/photos/" + i)
    try:
        # return render_template(name + ".html", title="Kvant", pics=pics)
        return render_template(name + ".html", title="Kvant", pics=pics, authenticated=current_user.is_authenticated)
    except jinja2.exceptions.TemplateNotFound:
        print(name + ".html")
        # return render_template("error_in_url.html", title="Kvant", ipc=ip_config)


@app.route("/pictures")
def pictures():
    pics = []
    for i in os.listdir("static/img/pics/"):
        pics.append("/static/img/pics/" + i)
    try:
        return render_template("pictures.html", title="Kvant", pics=pics)
    except jinja2.exceptions.TemplateNotFound:
        print("pictures.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Kvant',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Kvant',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.email = form.email.data
        user.hashed_password = generate_password_hash(form.password.data)
        user.rank = "client"
        db_sess.add(user)
        db_sess.commit()
        login_user(user, remember=True)
        cookie_saver(user.email, user.hashed_password)
        return redirect("/kvant")
    return render_template('register.html', title='Kvant', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/kvant")


@app.route("/")
def main_page():
    return redirect("/kvant")

    # return render_template("error_in_url.html", title="Kvant")


def main():
    db_session.global_init("db/users.db")
    app.run(port=ip_config["port"], host=ip_config["ip"])


if __name__ == '__main__':
    main()
