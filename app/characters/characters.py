from flask import Blueprint, render_template, url_for, redirect, flash
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired

from app.models.character import Character, db
from app.models.user import User


# Blueprint Configuration
character_bp = Blueprint('character_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
class AddCharacterForm(FlaskForm):
    """ Character Add Form """
    user_id = HiddenField()
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')


class EditCharacterForm(FlaskForm):
    """ Character Edit Form """
    id = HiddenField()
    # TODO: figure out how to remove the validate_choice field
    user_id = SelectField(label='User Name', coerce=int, validate_choice=False)
    character_name = StringField(label='Character Name')
    character_class = StringField(label='Character Class')
    is_active = BooleanField(label='Active')
    is_dead = BooleanField(label='Dead')


# Handlers
@character_bp.route('/character', methods=['GET'])
def show_character_list_form():
    """ Show list of current characters for user """

    # TODO: get current user from session
    user = User.query.filter_by(user_id=1).first()

    character_list = Character.query.all()
    return render_template('character_list.html', characters=character_list, user=user)


@character_bp.route('/character/add', methods=['GET', 'POST'])
def show_add_character_form():
    """ Show add character form and handle inserting new characters """

    # TODO: get current user from session
    user = User.query.filter_by(id=1).first()

    form = AddCharacterForm()
    if form.validate_on_submit():
        new_character = Character(
            user_id=int(form.user_id.data),
            character_name=form.character_name.data,
            character_class=form.character_class.data,
            is_active=True,
            is_dead=False
        )
        db.session.add(new_character)
        db.session.commit()
        flash('Character Added', 'success')
        return redirect(url_for('character_bp.show_character_list_form'))

    form.user_id.data = '1'
    return render_template('character_add.html', form=form, user=user)


@character_bp.route('/character/<id>', methods=['GET', 'POST'])
def show_character_edit_form(id):
    """ Show Character edit form and handle character updates """

    # TODO: Deal with character or user not found
    edit_character = Character.query.filter_by(id=id).first()
    user = User.query.filter_by(id=edit_character.user_id).first()

    user_list = [(x.firstname) for x in User.query.all()]

    user_list = User.query.with_entities(User.id, User.firstname).all()

    form = EditCharacterForm()

    if form.validate_on_submit():
        edit_character.id = int(form.id.data)
        edit_character.user_id = form.user_id.data
        edit_character.character_name = form.character_name.data
        edit_character.character_class = form.character_class.data
        edit_character.is_active = form.is_active.data
        edit_character.is_dead = form.is_dead.data
        db.session.commit()
        return redirect(url_for('character_bp.show_character_list_form'))
    else:
        form.process(obj=edit_character)
        form.user_id.choices = user_list
        return render_template('character_edit.html', form=form, character=edit_character, user=user)