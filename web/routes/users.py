from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash
from wtforms import StringField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, Email, Length

from web.models import User, db

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class UserAddForm(FlaskForm):
    """User Add Form"""
    user_id = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=20)])


class UserProfileForm(FlaskForm):
    """User Profile Form"""
    user_id = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=20)])


class LoginForm(FlaskForm):
    """Login Form"""
    user_id = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=20)])
    remember_me = BooleanField(label='Remember me')


# Handlers
@user_bp.route('/user', methods=['GET'])
@login_required
def show_user_list_form():
    """Show list of current users."""
    userList = User.query.all()
    return render_template('user/user_list.html', users=userList, user=current_user.firstname)


@user_bp.route('/user/profile/<user_id>', methods=['GET', 'POST'])
@login_required
def show_user_profile_form(user_id):
    """Show user edit form and handle user updates."""

    edit_user = User.query.filter_by(user_id=user_id).first()
    # TODO: deal with not getting a user back from the query

    form = UserProfileForm()
    if form.validate_on_submit():
        edit_user.user_id = form.email.data
        edit_user.password = form.password.data
        edit_user.firstname = form.firstname.data
        edit_user.lastname = form.lastname.data
        db.session.commit()
        return redirect(url_for('user_bp.show_user_list_form'))
    else:
        form.process(obj=edit_user)  # this provides the existing data to display on the form
        return render_template('user/user_edit.html', form=form, user=current_user.firstname)


@user_bp.route('/user/delete/<user_id>', methods=['GET'])
@login_required
def delete_confirm(user_id):
    """ Show Delete Confirmation Dialog """
    delete_user = User.query.get(user_id)
    if delete_user is not None:
        return render_template('user/user_delete.html', delete_user=delete_user, user=current_user.firstname)
    else:
        return redirect(url_for('user_bp.show_user_list_form'))


@user_bp.route('/user/delete/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user"""
    delete_user = User.query.get(user_id)

    if delete_user is not None:
        # Make sure we're not deleting ourselves
        if delete_user.user_id == current_user.user_id:
            flash('You cannot delete yourself!', 'warning')
        else:
            User.query.filter_by(user_id=user_id).delete()
            db.session.commit()
            flash('User Deleted', 'success')
    else:
        flash('User not found. No Action.', 'warning')
    return redirect(url_for('user_bp.show_user_list_form'))


def hash_password(cleartext_password):
    """ hash a password """
    hashed_password = generate_password_hash(cleartext_password)
    return hashed_password
