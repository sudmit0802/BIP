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
        return redirect(url_for('main'))
    else:
        return "user does not exist"
