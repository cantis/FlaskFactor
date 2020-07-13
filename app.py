import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf

app = app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
bs = Bootstrap(app)
fa = FontAwesome(app)
db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(64),
        index=False,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(32),
        index=False
    )


db.create_all()


class AddUserForm(FlaskForm):
    username = StringField(label='Username', validators=[InputRequired(), Email(message="I don\'t like your email.")])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=5, max=10), AnyOf(['secret', 'password'])])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/add', methods=['GET', 'POST'])
def show_add_user_form():
    """ Show user add form and handle inserting new users """
    form = AddUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return f'Form Successfully Submitted User:{username} Pass:{password}'
    return render_template('user_add.html', form=form)


@app.route('/user', methods=['GET'])
def show_user_list_form():
    """ Show list of current users """
    users = User.query.all()
    return render_template(
        'user_list.html',
        users=users
    )


if __name__ == '__main__':
    pass
