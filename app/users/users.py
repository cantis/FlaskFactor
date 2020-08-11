from flask import Blueprint, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Email, Length

from app.models.user import User, db

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class AddUserForm(FlaskForm):
    """Add User Form"""
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10)])


class EditUserForm(FlaskForm):
    """Edit User Form"""
    id = HiddenField()
    email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
    firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
    lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])
    password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10)])


# Handlers
@user_bp.route('/user', methods=['GET'])
def show_user_list_form():
    """Show list of current users."""
    userList = User.query.all()
    return render_template('user_list.html', users=userList)


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
        flash('User Added', 'success')
        return redirect(url_for('user_bp.show_user_list_form'))

    # if it's just a GET show the form
    return render_template('user_add.html', form=form)


@user_bp.route('/user/<id>', methods=['GET', 'POST'])
def show_edit_user_form(id):
    """Show user edit form and handle user updates."""

    edit_user = User.query.filter_by(id=id).first()
    # TODO: deal with not getting a user back from the query

    form = EditUserForm()

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


@user_bp.route('/user/delete/<id>', methods=['GET', 'POST'])
def delete_user(id):
    """Delete a user"""
    delete_user = User.query.filter_by(id=id).first()
    if delete_user is not None:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        flash('User Deleted', 'success')
    else:
        flash('User not found. No Action.', 'warning')
    return redirect(url_for('user_bp.show_user_list_form'))



