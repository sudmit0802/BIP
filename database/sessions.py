from .utils import *


def get_sessions_from_db(user_id):
    result = list()
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT id, tfv_address, tfv_time FROM tfv WHERE user_id={user_id};")
    rows = cur.fetchall()

    for row in rows:
        result.append(
            dict(id=f'{row[0]}', ip=row[1], time=row[2].strftime("%d %B %Y at %H:%M:%S")))
    cur.close()
    conn.close()

    if len(result) < 1:
        return None
    return result


def disable_user(user_id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"DELETE FROM tfv WHERE user_id={user_id};")
    conn.commit()
    cur.close()
    conn.close()
    return


def close_session(ip, id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"DELETE FROM tfv WHERE user_id={id} AND tfv_address = '{ip}';")
    conn.commit()
    cur.close()
    conn.close()
    return
