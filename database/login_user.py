from .utils import*
from auth.auth_utils import redirect, login_user, url_for
from .select_auth import select_auth
#from ...BIP import load_user


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


def get_user_email(login):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT email FROM users WHERE username = '{login}';")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0] 


def login_user_proxy(login, password):
    # Check if the login and password are valid (for example, by looking them up in a database)
    id = try_select_by_username(login)
    
    if id is None:
        return "Invalid login or password."
    
    user = select_auth(id)
    if user is not None and user.check_password(password):
        login_user(user)
        try:
            login_user(user)
        except Exception:
            return "Unable to login"
        try:
            email = get_user_email(user)
            #otp_secret = otp.generate_secret()
            #save_user_otp_email(username, email)
            #msg = Message('One-Time Password for Sign In', sender=app.config['MAIL_USERNAME'], recipients=[email])
            #msg.body = f'Your one-time password for sign in: {otp.generate_otp(otp_secret)}'
            #send_email(message, reciever)
        except Exception:
            return "Two-factor authentication fail"
        return redirect(url_for('verify', username=username))
    else:
        return "user does not exist"