from .auth_utils import *

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def check_password(self, password):
        return check_password_hash(self.password, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^[\x20-\x7E]+$', message='Username должен состоять только из ASCII printable символов'), Length(min=6, max=12, message="Длина username должна быть от 6 до 12 символов")] )
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Пароли должны совпадать'), Regexp(r'^[\x20-\x7E]+$', message='Пароль должен состоять только из ASCII printable символов'), Length(min=8, max=32, message="Длина пароля должна быть от 8 до 32 символов")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"placeholder": "Введите ваше имя"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Введите пароль"})
    submit = SubmitField('Войти')