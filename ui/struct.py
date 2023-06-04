from .ui_utils import *


class SessionsForm(FlaskForm):
    data = None
    exit_all = SubmitField('Выйти со всех устройств')


class PlansForm(FlaskForm):
    data = None
    create_plan = SubmitField('Создать новый план')


class NewPlanForm(FlaskForm):
    plan_name = StringField('Название плана',  render_kw={
                            "placeholder": "Название плана"})
    faculties = SelectField('Институт')
    groups = SelectField('Группа')
    confirm = SubmitField('Далее')


def get_subject_form_class(id):
    class_name = f'SubjectForm{id}'
    deadline_class = get_deadline_form_class(id)
    form_class = type(class_name, (FlaskForm,), {
                      'add': SubmitField('Добавить', name=f'add{id}', id=f'add{id}'), 'deadline': deadline_class()})
    return form_class


def get_deadline_form_class(id):
    class_name = f'DeadlineForm{id}'
    form_class = type(class_name, (FlaskForm,), {'name': StringField("Название работы", name=f'name{id}', id=f'name{id}', validators=[Length(min=3, max=32)],  render_kw={
        "placeholder": "Название работы"}), 'time': DateField("Дата дедлайна", name=f'time{id}', id=f'time{id}', format="%Y-%m-%d"), 'del': SubmitField('удалить', name=f'del{id}', id=f'del{id}')})  # эта кнопка без формы должна быть просто в html
    return form_class
