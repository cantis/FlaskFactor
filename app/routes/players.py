from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField
from wtforms.validators import InputRequired

from app.models.player import Player, db


# Blueprint Configuration
player_bp = Blueprint('player_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
class AddPlayerForm(FlaskForm):
    """ Player Add Form """
    firstname = StringField(label='First Name', validators=[InputRequired('First Name required')])
    lastname = StringField(label='Last Name', validators=[InputRequired('Last Name required')])


class EditPlayerForm(FlaskForm):
    """ Player Edit Form """
    id = HiddenField()
    firstname = StringField(label='First Name', validators=[InputRequired('First Name required')])
    lastname = StringField(label='Last Name', validators=[InputRequired('Last Name required')])
    is_active = BooleanField(label='Active')


# Handlers
@player_bp.route('/player', methods=['GET'])
@login_required
def show_player_list_form():
    """ Show list of players """
    player_list = Player.query.all()
    return render_template('player/player_list.html', players=player_list, user=current_user.firstname)


@player_bp.route('/player/add', methods=['GET', 'POST'])
@login_required
def show_player_add_form():
    """ Show player add form and handle add """
    form = AddPlayerForm()
    if form.validate_on_submit():
        new_player = Player(
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            is_active=True
        )
        db.session.add(new_player)
        db.session.commit()
        flash('Player Added', 'success')
        return redirect(url_for('player_bp.show_player_list_form'))

    return render_template('player/player_add.html', form=form, user=current_user.firstname)


@player_bp.route('/player/<id>', methods=['GET'])
@login_required
def show_player_edit_form(id):
    """ Show Player edit form"""
    # TODO: Handle player not found
    edit_player = Player.query.filter_by(id=id).first()
    form = EditPlayerForm()
    form.process(obj=edit_player)
    return render_template('player/player_edit.html', form=form, player=edit_player, user=current_user.firstname)


@player_bp.route('/player/<id>', methods=['POST'])
@login_required
def handle_player_edit_form(id):
    """ Handle updates on the player edit form"""

    edit_player = Player.query.filter_by(id=id).first()
    form = EditPlayerForm()

    if form.validate_on_submit():
        edit_player.id = int(form.id.data)
        edit_player.firstname = form.firstname.data
        edit_player.lastname = form.lastname.data
        edit_player.is_active = form.is_active.data
        db.session.commit()
        flash('Player Updated', 'success')

    return redirect(url_for('player_bp.show_player_list_form'))
