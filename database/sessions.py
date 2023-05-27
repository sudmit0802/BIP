from .utils import *


def get_sessions_from_db(user_id):
    result = list()
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT tfv_address, tfv_time FROM tfv WHERE user_id={user_id};")
    rows = cur.fetchall()
    id = 1
    for row in rows:
        result.append(
            dict(id=f'{id}', ip=row[0], time=row[1].strftime("%d %B %Y at %H:%M:%S")))
        id += 1
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
