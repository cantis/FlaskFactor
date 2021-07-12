from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from web.utility.setting import get_setting, save_setting
from web.models import Party

# Blueprint Configuration
home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static')


@home_bp.route('/', methods=['GET'])
@login_required
def index():
    ''' Homepage '''
    selected_id = get_setting('current_party')

    if selected_id:
        selected_party = Party.query.get(selected_id).party_name
    else:
        selected_party = 'Please Select'
    party_list = Party.query.all()
    return render_template('/home.html', current_user=current_user, party_menu=True, selected_party=selected_party, party_list=party_list)


@home_bp.route('/nav_select_party/<id>', methods=['GET'])
@login_required
def change_current_party(id):
    ''' Change the current party '''

    save_setting('current_party', id)

    return redirect(url_for('home_bp.index'))
