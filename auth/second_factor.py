from .auth_utils import redirect, url_for, render_template, login_user, session
from .auth import VerifyForm, generate_tf_code
from auth.smtp_routine import send_email
from database import get_connection, postgres_ctx, try_select_by_username, try_select_by_email, get_user_from_db, close_session
import datetime


def verify_user(username, ip):

    form = VerifyForm()

    id_un = try_select_by_username(username)
    id_em = try_select_by_email(username)
    id = id_un or id_em

    if id is None:
        return redirect(url_for('signin'))

    user = get_user_from_db(id)
    email = user.email

    try:
        # TODO Перенести в database
        conn = get_connection(postgres_ctx)
        cur = conn.cursor()
        result = cur.execute(
            f"SELECT tfv_time FROM tfv WHERE user_id = {id} AND tfv_address = '{ip}';")
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result is not None and session.get('tfv_code') is not None:

            tfv_time = result[0]
            time_diff = datetime.datetime.now() - tfv_time

            if time_diff.total_seconds() < 3600:
                login_user(user)
                return redirect(url_for('main'))
            session['tfv_code'] = None
            close_session(ip, id)

        if session.get('tfv_code') is None:
            code = generate_tf_code()
            msg = 'One-Time Password for Sign In: ' + code
            send_email(msg, email)
            session['tfv_code'] = code

    except Exception:
        return render_template('verify.html', form=form, message="Невозможно отправить код на вашу почту! Обратитесь в поддержку сайта.")

    if form.validate_on_submit():

        if form.verification_code.data != session.get('tfv_code'):
            return render_template('verify.html', form=form, message="Двухфакторная аутентификация не пройдена!")

        try:
            # TODO Перенести в database
            conn = get_connection(postgres_ctx)
            cur = conn.cursor()
            if result is None:
                cur.execute(
                    f"INSERT INTO tfv (tfv_code, tfv_time, tfv_address, user_id) VALUES ('{session.get('tfv_code')}', '{datetime.datetime.now()}', '{ip}', {id})")
            else:
                cur.execute(
                    f"UPDATE tfv SET tfv_code = '{session.get('tfv_code')}', tfv_time = '{datetime.datetime.now()}'; WHERE tfv_address = '{ip}' AND user_id = {id}")
            conn.commit()
            cur.close()
            conn.close()
            login_user(user)
            return redirect(url_for('main'))
        except Exception:
            return render_template('verify.html', form=form, message="Невозможно войти. Попробуйте позже.")

    if session.get('tfv_code') is None:
        return render_template('verify.html', form=form)

    return render_template('verify.html', form=form, notice="Вам на почту отправлен код подтверждения.")
