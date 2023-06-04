from .utils import *
import asyncio
from api_interface import get_subjects_routine


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


def get_plan_id_by_name(name):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT id FROM plans WHERE name='{name}';")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def push_subjects_for_group(group_id, plan_id):
    res = asyncio.run(get_subjects_routine(group_id))
    for subject in res:
        conn = get_connection(postgres_ctx)
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO subjects (name, plan_id) VALUES ('{subject}', {plan_id});")
        conn.commit()
        cur.close()
        conn.close()
    return


def push_plan(name, group_id, user_id):
    row = get_plan_id_by_name(name)
    if not row:
        conn = get_connection(postgres_ctx)
        cur = conn.cursor()
        cur.execute(
            f"INSERT INTO plans (name, status, user_id, group_id) VALUES ('{name}', 'active', {user_id}, '{group_id}');")
        conn.commit()
        cur.close()
        conn.close()
        row = get_plan_id_by_name(name)
        if row:
            push_subjects_for_group(group_id, int(row[0]))
            return row[0]
    return 0


def get_subjects_for_plan(plan_id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT id, name FROM subjects WHERE plan_id={plan_id};")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    subjects = dict()
    if not rows:
        return None
    for row in rows:
        subjects[row[0]] = row[1]
    return subjects


def get_stored_deadlines_for_subject(subject_id):

    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT id, specifier, deadline_time FROM deadlines WHERE subject_id={subject_id};")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    deadlines = list()
    for row in rows:
        deadlines.append(
            {'id': row[0], 'name': row[1], 'time': row[2].strftime("%d %B %Y")})

    return deadlines


def push_deadline(subject_id, spec, time):
    id = int(subject_id)
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"INSERT INTO deadlines (deadline_time, deadline_status, specifier, subject_id) VALUES ('{time} 12:00:00', true, '{spec}', {id});")
    conn.commit()
    cur.close()
    conn.close()
    return


def get_group_by_plan_id(plan_id):

    try:
        id = int(plan_id)
    except Exception:
        return None

    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(
        f"SELECT group_id FROM plans WHERE id={id};")
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return None
    return row[0]


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


def delete_deadline(deadline_id):
    conn = get_connection(postgres_ctx)
    cur = conn.cursor()
    cur.execute(f"DELETE FROM deadlines WHERE id={deadline_id};")
    conn.commit()
    cur.close()
    conn.close()
    return
