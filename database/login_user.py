from .utils import *
from auth import LoginForm, redirect, url_for, render_template, login_user, generate_tf_code, current_user
from .select_auth import get_user_from_db
from auth.smtp_routine import send_email


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


def get_user_email_by_id(id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT email FROM users WHERE id = {id};")
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
            try:
                email = get_user_email_by_id(id)
                code = generate_tf_code()

                conn = get_connection(postgres_ctx)
                cur = conn.cursor()

                cur.execute(
                    f"SELECT tfv_time FROM tfv WHERE user_id = {id} AND tfv_address = '{ip}';")
                result = cur.fetchone()
                if result is not None:
                    tfv_time = result[0]
                    current_time = datetime.datetime.now()
                    time_diff = current_time - tfv_time

                    if time_diff.total_seconds() < 3600:
                        login_user(user)
                        return redirect(url_for('main'))
                    else:
                        msg = 'One-Time Password for Sign In: ' + code
                        send_email(msg, email)
                        cur.execute(
                            f"UPDATE tfv SET tfv_code = '{code}', tfv_time = '{current_time}' WHERE user_id = {id} AND tfv_address = '{ip}';")
                else:
                    msg = 'One-Time Password for Sign In: ' + code
                    send_email(msg, email)
                    cur.execute(
                        f"INSERT INTO tfv (tfv_code, tfv_time, tfv_address, user_id) VALUES ('{code}', '{datetime.datetime.now()}', '{ip}', {id})")

                conn.commit()
                cur.close()
                conn.close()

            except Exception:
                return render_template('signin.html', form=form, message="Невозможно отправить код аутентификации.")

            return redirect(url_for('verify', username=username))

        else:
            return render_template('signin.html', form=form, message="Неверный логин или пароль!")

    return render_template('signin.html', form=form, message="")
