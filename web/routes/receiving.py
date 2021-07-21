''' Receive items from game session '''
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

from web import db
from web.models import Party
from web.utility.enums import ItemTypeEnum
from web.utility.setting import get_setting


# Blueprint Configuration
receiving_bp = Blueprint('receiving_bp', __name__, template_folder='templates', static_folder='static')

# Form Definitions


# Handlers
@receiving_bp.route('/receiving', methods=['GET', 'POST'])
@login_required
def show_receiving_list_form():
    ''' show form for items in a receipt '''
    mode = 'add'

    # Get current party selection and dropdown list
    selected_id = get_setting('current_party')
    if selected_id:
        selected_party = Party.query.get(selected_id).party_name
    else:
        selected_party = 'Please Select'
    party_list = Party.query.all()

    return render_template('receiving.html', mode=mode, current_user=current_user, party_menu=True, selected_party=selected_party, party_list=party_list)