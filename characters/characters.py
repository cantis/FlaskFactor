from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length
# from models import Character
#from . import db

# Blueprint Configuration
character_bp = Blueprint('character_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
# class AddUserForm(FlaskForm):
#     """ Character Form Fields """
#     email = StringField(label='Email', validators=[InputRequired('An email is required'), Email('Not an email format.')])
#     password = PasswordField(label='Password', validators=[InputRequired('Please enter a password'), Length(min=5, max=10), AnyOf(['secret', 'password'])])
#     firstname = StringField(label='First Name', validators=[InputRequired(message='A first name is required'), Length(min=1, max=20)])
#     lastname = StringField(label='Last Name', validators=[InputRequired('A last name is required'), Length(min=1, max=20)])


# Route Handlers
@character_bp.route('/character', methods=['GET'])
def show_character_list_form():
    """ Show list of current characters for user """
    # characters = Character.query.all()
    # return render_template('character_list.html'), characters=characters)
    return render_template('character_list.html')
