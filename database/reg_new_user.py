from .utils import*
from werkzeug.security import generate_password_hash
import auth
from flask import render_template, flash, redirect, url_for
import time

def reg_new_user():
    form = auth.RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data)
        conn = get_connection(postgres_ctx)
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        cur.close()
        conn.close()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('register_success'))
    return render_template('register.html', form=form)