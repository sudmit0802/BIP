from .ui_utils import *


class SessionsForm(FlaskForm):
    data = None
    exit_all = SubmitField('Выйти со всех устройств')


class PlansForm(FlaskForm):
    data = None
    create_plan = SubmitField('Создать новый план')
