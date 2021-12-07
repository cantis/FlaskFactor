from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField
from wtforms.validators import InputRequired, DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from web import db
from web.models import Character, Player, Party


# Blueprint Configuration
character_bp = Blueprint('character_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class AddCharacterForm(FlaskForm):
    """ Character Add Form """
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')
    # NOTE: the wtformst_sqlalchemy.fields is a bit of a hack from https://pypi.org/project/WTForms-SQLAlchemy/
    # this is becaue support for ORM-backed fields is depricated in wtforms.
    party_id = QuerySelectField(
        label='Party',
        get_label='party_name',
        query_factory=lambda: Party.query,
        validators=[DataRequired()]
    )
    player_id = QuerySelectField(
        label='Player',
        get_label='first_name',
        query_factory=lambda: Player.query,
        validators=[DataRequired()])


class EditCharacterForm(FlaskForm):
    """ Character Edit Form """
    id = HiddenField()
    character_name = StringField(label='Character Name', validators=[InputRequired('A Character name is required.')])
    character_class = StringField(label='Character Class')
    is_active = BooleanField(label='Active')
    is_dead = BooleanField(label='Dead')
    party_id = QuerySelectField(
        label='Party',
        get_label='party_name',
        query_factory=lambda: Party.query,
        validators=[DataRequired()]
    )
    player_id = QuerySelectField(
        label='Player',
        get_label='first_name',
        query_factory=lambda: Player.query,
        validators=[DataRequired()])


# Handlers
@character_bp.route('/character', methods=['GET'])
@login_required
def show_character_list_form():
    character_list = Character.query.all()
    form = AddCharacterForm()
    mode = 'add'
    return render_template('character.html', character_list=character_list, form=form, mode=mode,
                           current_user=current_user)


@character_bp.route('/character/add', methods=['POST'])
@login_required
def add_character():
    form = AddCharacterForm()

    if form.validate_on_submit():
        new_character = Character(
            character_name=form.character_name.data,
            character_class=form.character_class.data,
            player_id=form.player_id.data.id,
            party_id=form.party_id.data.id,
            is_active=True,
            is_dead=False
        )
        db.session.add(new_character)
        db.session.commit()
        flash('Character Added', 'success')

    return redirect(url_for('character_bp.show_character_list_form'))


@character_bp.route('/character/<id>', methods=['GET'])
@login_required
def player_edit_form_get(id):
    ''' Show Character edit form '''
    character = Character.query.get(id)
    character_list = Character.query.all()
    mode = 'edit'
    form = EditCharacterForm()
    form.process(obj=character_list)
    form.process(obj=character)
    return render_template('character.html', character_list=character_list, character=character, form=form, mode=mode, current_user=current_user)


@character_bp.route('/character/<id>', methods=['POST'])
@login_required
def character_edit_form(id):
    """ Handle editing a character """

    # TODO: Deal with character or user not found
    edit_character = Character.query.filter_by(id=id).first()
    if not edit_character:
        raise IndexError(f'Index {id} not found')

    form = EditCharacterForm()

    if form.validate_on_submit():
        edit_character.id = int(form.id.data)
        edit_character.character_name = form.character_name.data
        edit_character.character_class = form.character_class.data
        edit_character.is_active = form.is_active.data
        edit_character.is_dead = form.is_dead.data
        edit_character.party_id = form.party_id.data.id
        edit_character.player_id = form.player_id.data.id
        db.session.commit()
        return redirect(url_for('character_bp.show_character_list_form'))
    else:
        # Back to edit mode, validation failed.
        character_list = Character.query.all()
        mode = 'edit'
        form = EditCharacterForm()
        form.process(obj=character_list)
        form.process(obj=edit_character)
        return render_template('character/character_edit.html', form=form, character=edit_character, mode=mode, current_user=current_user)


