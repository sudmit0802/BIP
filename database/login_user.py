from .utils import*
from auth import LoginForm, redirect, login_user, url_for, render_template
from .select_auth import select_auth


def try_select_by_username(login):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM users WHERE username = '{login}';")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0] 


def login_user_proxy():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        id = try_select_by_username(username)
        if id is None:
            return render_template('signin.html', form=form, not_exist = "Неверный логин или пароль!", login_exception="")
    
        user = select_auth(id)
        if user is not None and user.check_password(password):
            try:
                login_user(user)
            except Exception:
                return render_template('signin.html', form=form, not_exists="", login_exception = "Невозможно войти. Попробуйте позже.")
            return redirect(url_for('main'))
        else:
            return render_template('signin.html', form=form, not_exist = "Неверный логин или пароль!", login_exception="")

    return render_template('signin.html', form=form)
