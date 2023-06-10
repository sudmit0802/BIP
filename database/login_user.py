from .utils import *
from auth import LoginForm, redirect, url_for, render_template
from .select_auth import get_user_from_db


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


def try_select_by_email(email):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT id FROM users WHERE email = '{email}';")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0]


def login_user_proxy(ip):
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        id_us = try_select_by_username(username)
        id_em = try_select_by_email(username)
        if id_em is None and id_us is None:
            return render_template('signin.html', form=form, message="Неверный логин или пароль!!!")

        id = id_us or id_em
        user = get_user_from_db(id)

        if user is not None and user.check_password(password):
            return redirect(url_for('verify', username=username))
        return render_template('signin.html', form=form, message="Неверный логин или пароль!")

    return render_template('signin.html', form=form, message="")
