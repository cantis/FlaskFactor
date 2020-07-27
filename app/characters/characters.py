from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField

from app.models.character import Character


# Blueprint Configuration
character_bp = Blueprint('character_bp', __name__, template_folder='templates', static_folder='static')


# Form Definition
class CharacterListForm(FlaskForm):
    """ Character List Form Fields """
    user = StringField(label='User')
    characters = StringField(label="Character Name")


# Route Handlers
@character_bp.route('/character', methods=['GET'])
def show_character_list_form():
    """ Show list of current characters for user """
    characters = Character.query.all()
    form = CharacterListForm()
    return render_template('character_list.html', form=form)
