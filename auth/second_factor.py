from .auth_utils import redirect, url_for, render_template, login_user
from .auth import VerifyForm
from database import get_tfv_code_by_username, try_select_by_username, select_auth

def verify_user(username):
    form = VerifyForm()
    if form.validate_on_submit():
        verification_code = form.verification_code.data
        code_from_db = get_tfv_code_by_username(username)
        if verification_code != code_from_db:
            return render_template('signin.html', form=form, message = "Двухфакторная аутентификация не пройдена!")
        try:
            id = try_select_by_username(username)
            if id is None:
                return render_template('signin.html', form=form, message = "Что-то пошло не так)")
            user = select_auth(id)
            login_user(user)
        except Exception:
            return render_template('signin.html', form=form, message = "Невозможно войти. Попробуйте позже.")
        
        return redirect(url_for('main')) 
    return render_template('verify.html', form=form)