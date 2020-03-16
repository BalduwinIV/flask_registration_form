from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired
from data import db_session
from data.users import *


app = Flask(__name__)
app.config["SECRET_KEY"] = 'yandexlyceum_secret_key'


class RegisterForm(FlaskForm):
    email = StringField('Login / Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat password', validators=[DataRequired()])
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    speciality = StringField('Speciality', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.repeat_password.data:
            return render_template('index.html', title='Log in', form=form,
                                   message='Passwords are different')
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('index.html', title='Log in', form=form,
                                   message='This email has already used by another user')
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=int(form.age.data),
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('index.html', title='Log in', form=form)


@app.route('/login')
def login():
    return render_template('login.html', title='Completed')


if __name__ == '__main__':
    db_session.global_init("db/jobs.sqlite")
    app.run()