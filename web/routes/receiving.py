''' Receive items from game session '''
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.fields.core import FloatField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, NumberRange, Optional

from web import db
from web.models import Party, Receiving
from web.utility.enums import ItemTypeEnum
from web.utility.setting import get_common_setting


# Blueprint Configuration
receiving_bp = Blueprint('receiving_bp', __name__, template_folder='templates', static_folder='static')


# Form Definitions
class AddItemForm(FlaskForm):
    ''' Form for adding receiving items '''
    item_name = StringField(label='Name', validators=[DataRequired()])
    # type = SelectField('Type', choices=ItemTypeEnum.choices(), validators=[DataRequired()])
    type = StringField(label='Type', validators=[DataRequired()])
    quantity = IntegerField(label='Count', validators=[DataRequired(), NumberRange(min=1)])
    value = FloatField(label='Value', validators=[Optional()])
    saleValue = FloatField(label='SaleValue', validators=[Optional()])
    submit = SubmitField(label='Submit')


class EditItemForm(FlaskForm):
    ''' Form for editing receiving items '''
    id = HiddenField()
    item_name = StringField('Name', validators=[DataRequired()])
    # type = SelectField('Type', choices=ItemTypeEnum.choices(), validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    quantity = IntegerField('Count', validators=[DataRequired(), NumberRange(min=1)])
    value = FloatField('Value', validators=[Optional()])
    salevalue = FloatField('Sale Value', validators=[Optional()])
    submit = SubmitField('Submit')


# Handlers
@receiving_bp.route('/receiving', methods=['GET'])
@login_required
def show_receiving_list_form():
    ''' show form for items in a receipt, set to add mode to receive items '''
    mode = 'add'
    form = AddItemForm()

    # Party list and current party selection
    party_list = Party.query.all()
    selected_party_id = get_common_setting(setting_name='current_party')
    if selected_party_id:
        selected_party = Party.query.get(selected_party_id).party_name
    else:
        selected_party = 'Please Select'  # TODO: if no party selected, show dialog prompting to select one

    # Receiving list data
    received = Receiving.query.filter_by(party_id=selected_party_id, ).all()

    # Show the form
    return render_template('receiving.html', mode=mode, current_user=current_user, party_menu=True,
                           selected_party=selected_party, party_list=party_list, received=received, form=form)


@receiving_bp.route('/receiving/add', methods=['POST'])
@login_required
def add_receiving_item():
    ''' add receiving item to database '''
    form = AddItemForm()
    if form.validate_on_submit():
        # Get party id
        party_id = get_common_setting(setting_name='current_party')

        # Create new receiving item
        new_receiving = Receiving(id=next_receiving_id(party_id), party_id=party_id, name=form.name.data,
                                  type=form.type.data, quantity=form.quantity.data, value=form.value.data,
                                  salevalue=form.saleValue.data)

        # Add to database
        db.session.add(new_receiving)
        db.session.commit()

    # Redirect to receiving list
    return redirect(url_for('receiving_bp.show_receiving_list_form'))

    # Show the form again
    # return render_template('receiving.html', mode='add',
    #                        current_user=current_user, party_menu=True, form=form)


# Utility
def next_receiving_id(selected_party_id):
    ''' get next receiving id '''
    max_id = db.session.query(db.func.max(Receiving.id)).filter_by(party_id=selected_party_id).scalar()
    if max_id:
        return max_id + 1
    else:
        return 1
