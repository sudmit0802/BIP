from .utils import *
from auth import User


def get_user_from_db(user_id):

    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE id = {user_id}")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return User(row[0], row[1], row[2], row[3])


def get_tfv_code_by_username(username, ip):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT tfv_code FROM tfv WHERE tfv_address = '{ip}' AND user_id = (SELECT id FROM users WHERE username = '{username}');")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0]


def get_tfv_code_by_email(username, ip):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT tfv_code FROM tfv WHERE tfv_address = '{ip}' AND user_id = (SELECT id FROM users WHERE email = '{username}');")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0]
