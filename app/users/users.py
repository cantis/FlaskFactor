from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, Email, Length

from app.models.user import User, db

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class UserAddForm(FlaskForm):
    """User Add Form"""
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10)])


class UserProfileForm(FlaskForm):
    """User Profile Form"""
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10)])


class LoginForm(FlaskForm):
    """Login Form"""
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10)])
    remember_me = BooleanField(label='Remember me')


# Handlers
@user_bp.route('/user', methods=['GET'])
@login_required
def show_user_list_form():
    """Show list of current users."""
    userList = User.query.all()
    return render_template('user_list.html', users=userList)


@user_bp.route('/user/register', methods=['GET', 'POST'])
def show_user_register_form():
    """Show user add form and handle inserting new users."""

    form = UserAddForm()
    # check and see if it's a POST, i.e. it's a form submit
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        firstname = form.firstname.data
        lastname = form.lastname.data
        new_user = User(email=email, password=password, firstname=firstname, lastname=lastname)
        db.session.add(new_user)
        db.session.commit()
        flash('User Added', 'success')
        return redirect(url_for('user_bp.show_user_list_form'))

    # if it's just a GET show the form
    return render_template('user_add.html', form=form)


@user_bp.route('/user/profile', methods=['GET', 'POST'])
@login_required
def show_user_profile_form(email):
    """Show user edit form and handle user updates."""

    edit_user = User.query.filter_by(email=email).first()
    # TODO: deal with not getting a user back from the query

    form = UserProfileForm()
    if form.validate_on_submit():
        edit_user.email = form.email.data
        edit_user.password = form.password.data
        edit_user.firstname = form.firstname.data
        edit_user.lastname = form.lastname.data
        db.session.commit()
        return redirect(url_for('user_bp.show_user_list_form'))
    else:
        form.process(obj=edit_user)  # this provides the existing data to display on the form
        return render_template('user_edit.html', form=form, user=edit_user)


@user_bp.route('/user/delete/<email>', methods=['GET', 'POST'])
@login_required
def delete_user(email):
    """Delete a user"""
    delete_user = User.query.get(email=email)
    if delete_user is not None:
        User.query.get(email=email).delete()
        db.session.commit()
        flash('User Deleted', 'success')
    else:
        flash('User not found. No Action.', 'warning')
    return redirect(url_for('user_bp.show_user_list_form'))


@user_bp.route('/login', methods=['GET', 'POST'])
def show_login_form():
    """ For GET requests, display the login form.
    for POST, process the form.
    """
    form = LoginForm()

    # handle if user is already logged in and they hit the login url send them home
    if current_user.is_authenticated:
        return redirect(url_for('home_bp.index'))

    if form.validate_on_submit():
        # POST Request, confirm password and log in if ok
        user = User.query.get(form.email.data)
        if user is None or not user.is_password_valid(user.password, form.password.data):
            flash('Invalid username or password.')
            return redirect(url_for('show_login_form'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home_bp.index'))

    # GET request, show the login form
    return render_template('login.html', form=form)


def is_password_valid(hashed_password, input_password):
    result = check_password_hash(hashed_password, input_password)
    return result


def hash_password(cleartext_password):
    """ hash a password """
    hashed_password = generate_password_hash(cleartext_password)
    return hashed_password

@user_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """Logout Current User."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template('logout.html')
