from flask import Blueprint, render_template
# from flask_login import current_user, login_required


# Blueprint Configuration
home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static')


@home_bp.route('/', methods=['GET'])
# @login_required
def index():
    """ Homepage """
    # return render_template('home/home.html', user=current_user.firstname)
    return render_template('home/home.html', user='<not set>')
