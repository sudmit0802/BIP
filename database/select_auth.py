from .utils import*
from auth import User

def select_auth(user_id):
    
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return User(row[0], row[1], row[2], row[3], row[4])
            

def get_tfv_code_by_username(username):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT tfv_code FROM users WHERE username = '{username}';")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0] 
