from flask import Blueprint, render_template
from flask_login import current_user, login_required
from web.utility.setting import save_setting


# Blueprint Configuration
home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static')


@home_bp.route('/', methods=['GET'])
@login_required
def index():
    ''' Homepage '''
    return render_template('/home.html', current_user=current_user)


@home_bp.route('/nav_select_party/<id>', methods=['GET'])
@login_required
def change_current_party(id):
    ''' Change the current party '''

    save_setting('current_party', id)
    return render_template('/home.html', current_user=current_user)
