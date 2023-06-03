import asyncpg


async def create_a_report():
    conn = await asyncpg.connect(user="postgres", password="0802", database="lab_manager_database", host="127.0.0.1")
    values = await conn.fetch("""select * from users""")
    await bot.send_message(404247225, values)
    await conn.close()


