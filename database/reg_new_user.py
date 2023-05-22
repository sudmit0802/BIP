from .utils import *
from auth import RegistrationForm, render_template, generate_password_hash
from flask import render_template
from .login_user import try_select_by_username, try_select_by_email


def reg_new_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
        id_usrname = try_select_by_username(username)
        id_email = try_select_by_email(email)

        if id_usrname or id_email:
            return render_template('signup.html', form=form, message="Пользователь с таким именем уже существует!")

        conn = get_connection(postgres_ctx)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, username, password) VALUES (%s, %s, %s)",
                    (email, username, password))
        conn.commit()
        cur.close()
        conn.close()
        return render_template('signup.html', form=form, message="Регистрация прошла успешно! Теперь вы можете: ")
    return render_template('signup.html', form=form, message="Уже есть аккаунт?")
