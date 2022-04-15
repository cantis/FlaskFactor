from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField
from wtforms.fields.core import BooleanField
from wtforms.validators import InputRequired, Email

from web import db
from web.models import Player


# Blueprint Configuration
player_bp = Blueprint('player_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class AddPlayerForm(FlaskForm):
    """ Player Add Form """
    first_name = StringField(label='First Name', validators=[InputRequired('First Name required')])
    last_name = StringField(label='Last Name', validators=[InputRequired('Last Name required')])
    email = StringField(label='Email', validators=[InputRequired('Please add an email.'), Email('Invalid email format')])


class EditPlayerForm(FlaskForm):
    """ Player Edit Form """
    id = HiddenField()
    first_name = StringField(label='First Name', validators=[InputRequired('First Name required')])
    last_name = StringField(label='Last Name', validators=[InputRequired('Last Name required')])
    email = StringField(label='Email', validators=[InputRequired('Please add an email.'), Email('Invalid email format')])
    is_active = BooleanField(label='Active', false_values={'false', ''})


# Handlers
@player_bp.route('/player', methods=['GET'])
@login_required
def player_form():
    """ Show list of players """
    player_list = Player.query.all()
    form = AddPlayerForm()
    mode = 'add'
    return render_template('player.html', player_list=player_list, current_user=current_user, mode=mode, form=form)


@player_bp.route('/player/add', methods=['POST'])
@login_required
def add_player():
    """ Process adding a player """
    form = AddPlayerForm()
    if form.validate_on_submit():
        new_player = Player(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            is_active=True
        )
        db.session.add(new_player)
        db.session.commit()
        flash('Player Added', 'success')

    return redirect(url_for('player_bp.player_form'))


@player_bp.route('/player/<id>', methods=['GET'])
@login_required
def player_edit_form_get(id):
    """ Show Player form in edit mode """
    # TODO: Handle player not found
    player = Player.query.get(id)
    player_list = Player.query.all()
    mode = 'edit'
    form = EditPlayerForm()
    form.process(obj=player_list)
    form.process(obj=player)
    return render_template('player.html', player_list=player_list, player=player, form=form, mode=mode, current_user=current_user)


@player_bp.route('/player/<id>', methods=['POST'])
@login_required
def player_edit_form_post(id):
    """ Handle updates on the player edit form """
    player = Player.query.get(id)
    player_list = Player.query.all()
    form = EditPlayerForm()

    mode = ''

    if form.validate_on_submit():
        player.id = int(form.id.data)
        player.first_name = form.first_name.data
        player.last_name = form.last_name.data
        player.email = form.email.data
        player.is_active = form.is_active.data
        db.session.commit()
        flash('Player Updated', 'success')
        mode = 'add'
    else:
        # We end up back in edit mode if we don't validate
        form.process(obj=player_list)
        form.process(obj=player)
        mode = 'edit'

    # show the player form, mode from validate above
    return render_template('player.html', player_list=player_list, player=player, form=form, mode=mode, current_user=current_user)
