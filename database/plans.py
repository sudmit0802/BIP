from .utils import *


def get_plans_from_db(user_id):
    result = list()
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT id, name, status FROM plans WHERE user_id={user_id} ORDER BY id;")
    rows = cur.fetchall()

    for row in rows:
        result.append(
            dict(id=f'{row[0]}', name=row[1], status=row[2]))
    cur.close()
    conn.close()

    if len(result) < 1:
        return None
    return result


def delete_plan(plan_id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    id = int(plan_id)
    cur.execute(f"DELETE FROM plans WHERE id={id};")
    conn.commit()
    cur.close()
    conn.close()
    return


def mute_plan(plan_id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    id = int(plan_id)
    cur.execute(f"UPDATE plans SET status='muted' WHERE id={id};")
    conn.commit()
    cur.close()
    conn.close()
    return


def unmute_plan(plan_id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    id = int(plan_id)
    cur.execute(f"UPDATE plans SET status='active' WHERE id={id};")
    conn.commit()
    cur.close()
    conn.close()
    return
