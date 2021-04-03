from flask import Blueprint, render_template


error_bp = Blueprint('error_bp', __name__, template_folder='templates', static_folder='static')


@error_bp.app_errorhandler(404)
def erorr_404(error):
    return render_template('error/404.html'), 404


@error_bp.app_errorhandler(403)
def erorr_403(error):
    return render_template('error/403.html'), 403


@error_bp.app_errorhandler(500)
def erorr_500(error):
    return render_template('error/500.html'), 500
