from flask import Blueprint, render_template
import werkzeug


error_bp = Blueprint(
    'error_bp', __name__, template_folder='templates', static_folder='static'
)


@error_bp.app_errorhandler(werkzeug.exceptions.Unauthorized)
def erorr_401(error):
    '''Unauthorized Error'''
    return render_template('error/401.html'), 401


@error_bp.app_errorhandler(werkzeug.exceptions.NotFound)
def erorr_404(error):
    '''Not Found Error'''
    return render_template('error/404.html'), 404


@error_bp.app_errorhandler(werkzeug.exceptions.Forbidden)
def erorr_403(error):
    '''Forbidden Error'''
    return render_template('error/403.html'), 403


@error_bp.app_errorhandler(werkzeug.exceptions.InternalServerError)
def erorr_500(error):
    return render_template('error/500.html'), 500
