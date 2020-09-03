from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired

from app.models.character import Character, db
from app.models.player import Player


# Blueprint Configuration
character_bp = Blueprint('character_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
class AddCharacterForm(FlaskForm):
    """ Character Add Form """
    player_id = SelectField(label='Player', coerce=int)
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')


class EditCharacterForm(FlaskForm):
    """ Character Edit Form """
    id = HiddenField()
    player_id = SelectField(label='Player', coerce=int)
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')
    is_active = BooleanField(label='Active')
    is_dead = BooleanField(label='Dead')


# Handlers
@character_bp.route('/character', methods=['GET'])
@login_required
def show_character_list_form():
    """ Show list of current characters for user """
    character_list = Character.query.all()
    return render_template('character_list.html', characters=character_list, user=current_user.firstname)


@character_bp.route('/character/add', methods=['GET', 'POST'])
@login_required
def show_add_character_form():
    """ Show add character form and handle inserting new characters """

    form = AddCharacterForm()
    player_list = Player.query.with_entities(Player.id, Player.firstname)
    form.player_id.choices = player_list

    if form.validate_on_submit():
        new_character = Character(
            player_id=form.player_id.data,
            character_name=form.character_name.data,
            character_class=form.character_class.data,
            is_active=True,
            is_dead=False
        )
        db.session.add(new_character)
        db.session.commit()
        flash('Character Added', 'success')
        return redirect(url_for('character_bp.show_character_list_form'))

    return render_template('character_add.html', form=form, user=current_user.firstname)


@character_bp.route('/character/<id>', methods=['GET', 'POST'])
@login_required
def show_character_edit_form(id):
    """ Show Character edit form and handle character updates """

    # TODO: Deal with character or user not found
    edit_character = Character.query.filter_by(id=id).first()

    form = EditCharacterForm()

    if form.validate_on_submit():
        edit_character.id = int(form.id.data)
        edit_character.player_id = form.player_id.data
        edit_character.character_name = form.character_name.data
        edit_character.character_class = form.character_class.data
        edit_character.is_active = form.is_active.data
        edit_character.is_dead = form.is_dead.data
        db.session.commit()
        return redirect(url_for('character_bp.show_character_list_form'))
    else:
        player_list = Player.query.with_entities(Player.id, Player.firstname)
        form.player_id.choices = player_list
        form.process(obj=edit_character)
        return render_template('character_edit.html', form=form, character=edit_character, user=current_user.firstname)