from .ui_utils import *


class SessionsForm(FlaskForm):
    data = None
    exit_all = SubmitField('Выйти со всех устройств')
