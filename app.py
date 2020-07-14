from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_fontawesome import FontAwesome
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf


app = app = Flask(__name__)
app.config.from_object('config.DevConfig')
app.app_context().push()

bs = Bootstrap(app)

fa = FontAwesome(app)

db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    """ Data model for user account """
    __tablename__ = 'users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    username = db.Column(
        db.String(20),
        index=False,
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(32),
        index=False
    )
    firstname = db.Column(
        db.String(20)
    )
    lastname = db.Column(
        db.String(20)
    )


db.create_all()


class AddUserForm(FlaskForm):
    """ User Form Fields """
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10), AnyOf(['secret', 'password'])])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])


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
        firstname = form.firstname.data
        lastname = form.lastname.data
        new_user = User(username=username, password=password, firstname=firstname, lastname=lastname)
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
