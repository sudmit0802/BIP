from .auth_utils import *


class User(UserMixin):
    def __init__(self, id, email, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.email = email

    def check_password(self, password):
        return check_password_hash(self.password, password)


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()], render_kw={
                        "placeholder": "Введите почту (email)"})
    username = StringField('Username', validators=[DataRequired(), Regexp(r'^[\x20-\x7E]+$', message='Username должен состоять только из ASCII printable символов'), Length(
        min=6, max=12, message="Длина username должна быть от 6 до 12 символов")], render_kw={"placeholder": "Придумайте имя пользователя (логин)"})
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Пароли должны совпадать'), Regexp(
        r'^[\x20-\x7E]+$', message='Пароль должен состоять только из ASCII printable символов'), Length(min=8, max=32, message="Длина пароля должна быть от 8 до 32 символов")], render_kw={"placeholder": "Придумайте пароль"})
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired()], render_kw={"placeholder": "Подтвердите пароль"})
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={
                           "placeholder": "Введите email или логин"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={
                             "placeholder": "Введите пароль"})
    submit = SubmitField('Войти')


class VerifyForm(FlaskForm):
    verification_code = StringField('Code', validators=[DataRequired(), Length(
        min=6, max=6)], render_kw={"placeholder": "Введите код подтверждения"})
    submit = SubmitField('Подтвердить')


def generate_tf_code():
    code = ''
    for i in range(6):
        code += str(random.randrange(10))
    return code
