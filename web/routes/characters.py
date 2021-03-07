from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField, IntegerField
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired

from web import db
from web.models import Character, Player, Party


# Blueprint Configuration
character_bp = Blueprint('character_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class AddCharacterForm(FlaskForm):
    """ Character Add Form """
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')
    party_id = SelectField(label='Party',  coerce=int)
    player_id = SelectField(label='Player', coerce=int)


class EditCharacterForm(FlaskForm):
    """ Character Edit Form """
    id = HiddenField()
    player_id = SelectField(label='Player', coerce=int)
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')
    is_active = BooleanField(label='Active')
    is_dead = BooleanField(label='Dead')
    party_id = SelectField(label='Party', coerce=int)


# Handlers
@character_bp.route('/character', methods=['GET'])
# @login_required
def show_character_list_form():
    character_list = Character.query.all()
    form = AddCharacterForm()
    form.player_id.choices = [(pl.id, pl.first_name) for pl in Player.query.all()]
    form.party_id.choices = [(pa.id, pa.party_name) for pa in Party.query.all()]
    mode = 'add'
    return render_template('character.html', character_list=character_list, form=form, mode=mode,
                           current_user=current_user)


@character_bp.route('/character/add', methods=['POST'])
# @login_required
def add_character():
    form = AddCharacterForm()

    if form.validate_on_submit():
        new_character = Character(
            character_name=form.character_name.data,
            character_class=form.character_class.data,
            player_id=form.player_id.data,
            party_id=form.party_id.data,
            is_active=True,
            is_dead=False
        )
        db.session.add(new_character)
        db.session.commit()
        flash('Character Added', 'success')

    return redirect(url_for('character_bp.show_character_list_form'))


# @character_bp.route('/character/<id>', methods=['GET', 'POST'])
# # @login_required
# def show_character_edit_form(id):
#     """ Show Character edit form and handle character updates """

#     # TODO: Deal with character or user not found
#     edit_character = Character.query.filter_by(id=id).first()

#     form = EditCharacterForm()

#     if form.validate_on_submit():
#         edit_character.id = int(form.id.data)
#         edit_character.player_id = form.player_id.data
#         edit_character.character_name = form.character_name.data
#         edit_character.character_class = form.character_class.data
#         edit_character.is_active = form.is_active.data
#         edit_character.is_dead = form.is_dead.data
#         edit_character.party_id = form.party_id.data
#         db.session.commit()
#         return redirect(url_for('character_bp.show_character_list_form'))
#     else:
#         player_list = Player.query.with_entities(Player.id, Player.firstname)
#         form.player_id.choices = player_list
#         party_list = Party.query.with_entities(Party.id, Party.party_name)
#         form.party_id.choices = party_list
#         form.process(obj=edit_character)
#         return render_template('character/character_edit.html', form=form, character=edit_character, user=current_user.firstname)
