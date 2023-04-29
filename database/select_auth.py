from .utils import*
import auth

def select_auth(user_id):
    
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return auth.User(row[0], row[1], row[2])
            