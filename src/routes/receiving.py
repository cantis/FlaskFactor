from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask_wtf import FlaskForm


# Blueprint Configuration
receiving_bp = Blueprint(
    'receiving_bp', __name__, template_folder='templates', static_folder='static'
)


# Form Definitions
class AddReceivingForm(FlaskForm):
    pass


class EditReceivingForm(FlaskForm):
    pass


# Route Definitions
@receiving_bp.route('/receiving', methods=['GET'])
@login_required
def receivin_list():
    mode = 'add'
    return render_template(
        'receiving.html', mode=mode, current_user=current_user
    )
