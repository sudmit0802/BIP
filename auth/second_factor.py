from .auth_utils import redirect, url_for, render_template, login_user
from .auth import VerifyForm, LoginForm
from database import get_tfv_code_by_username, get_tfv_code_by_email, try_select_by_username, try_select_by_email, get_user_from_db

# TODO redirects instead of render_templates


def verify_user(username, ip):
    form = VerifyForm()
    if form.validate_on_submit():
        verification_code = form.verification_code.data

        code_from_db_by_username = get_tfv_code_by_username(username, ip)
        code_drom_db_by_email = get_tfv_code_by_email(username, ip)

        code_from_db = code_from_db_by_username or code_drom_db_by_email

        if verification_code != code_from_db:
            return render_template('signin.html', form=LoginForm(), message="Двухфакторная аутентификация не пройдена!")
        try:
            id_un = try_select_by_username(username)
            id_em = try_select_by_email(username)
            id = id_un or id_em
            if id is None:
                return redirect(url_for('signin'))
            user = get_user_from_db(id)
            login_user(user)
        except Exception:
            return render_template('signin.html', form=LoginForm(), message="Невозможно войти. Попробуйте позже.")

        return redirect(url_for('main'))
    return render_template('verify.html', form=form)
