from flask import render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from . import app, db
from models import User


class AddUserForm(FlaskForm):
    """ User Form Fields """
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10), AnyOf(['secret', 'password'])])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])


@app.route('/user/add', methods=['GET', 'POST'])
def show_add_user_form():
    """ Show user add form and handle inserting new users """
    form = AddUserForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(new_user)
        db.session.commit()
        return f'Form Successfully Submitted User:{email} Pass:{password}'
    return render_template('user_add.html', form=form)


@app.route('/user', methods=['GET'])
def show_user_list_form():
    """ Show list of current users """
    users = User.query.all()
    return render_template(
        'user_list.html',
        users=users
    )
