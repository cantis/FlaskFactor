from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, BooleanField, validators
from wtforms.fields.core import SelectField
from wtforms.validators import InputRequired

from app.models.party import Party, db
from app.models.character import Character


# Blueprint Configuration
party_bp = Blueprint('party_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
class AddPartyForm(FlaskForm):
    """ Party Add Form """
    party_name = StringField(label='Party Name', validators=[InputRequired('A Party Name is required.')])


class EditPartyForm(FlaskForm):
    """ Party Edit Form """    
    id = HiddenField()
    party_name = StringField(label='Party Name', validators=[InputRequired('A Party Name is required.')])
    is_active = BooleanField(label='Active')


# Handlers
@party_bp.route('/party', methods=['GET'])
@login_required
def show_party_list_form():
    """ Show list of Adventuring Parties """
    party_list = Party.query.all()
    return render_template('party/party_list.html', parties=party_list, user=current_user.firstname)


@party_bp.route('/party/add', methods=['GET', 'POST'])
@login_required
def show_party_add_form():
    """ Show add party form and handle inserting new party """
    form = AddPartyForm()

    if form.validate_on_submit():
        new_party = Party(
            party_name=form.party_name.data,
            is_active=True
        )
        db.session.add(new_party)
        db.session.commit()
        flash('Party Added', 'success')
        return redirect(url_for('party_bp.show_party_list_form'))
    return render_template('party/party_add.html', form=form, user=current_user.firstname)


@party_bp.route('/party/<id>', methods=['GET', 'POST'])
@login_required
def show_party_edit_form(id):
    """ Show party edit form and handle updates """
    form = EditPartyForm()
    edit_party = Party.query.filter_by(id=id).first()

    if form.validate_on_submit():
        edit_party.party_name = form.party_name.data
        edit_party.is_active = form.is_active.data
        db.session.commit()
        return redirect(url_for('party_bp.show_party_list_form'))
    else:
        form.process(obj=edit_party)
        return render_template('party/party_edit.html', form=form, party=edit_party, user=current_user.firstname)
