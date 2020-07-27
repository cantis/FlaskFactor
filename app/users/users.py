from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf

from app.models.user import User, db

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
class AddUserForm(FlaskForm):
    """Add User Form Declaration"""
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10), AnyOf(['secret', 'password'])])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])


# class ListUsersForm(FlaskForm):
#     """List Users Form Declaration"""



# Handlers
@user_bp.route('/user/add', methods=['GET', 'POST'])
def show_add_user_form():
    """Show user add form and handle inserting new users."""

    form = AddUserForm()
    # check and see if it's a POST, i.e. it's a form submit
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(new_user)
        db.session.commit()
        # return f'Form Successfully Submitted User:{email} Pass:{password}'
        return redirect(url_for('user_list.html'))

    # if it's just a GET show the form
    return render_template('user_add.html', form=form)


@user_bp.route('/user', methods=['GET'])
def show_user_list_form():
    """Show list of current users."""
    users = User.query.all()
    return render_template('user_list.html', users=users)
