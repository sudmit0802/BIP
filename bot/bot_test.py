import asyncio
import asyncpg
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from datetime import datetime

# Update listeners are functions that are called when any update is received.

bot = AsyncTeleBot(token='6236134779:AAF9IVmzQl2vAz9e5U8BCG8bqGECE_RzSUw')


@bot.message_handler(commands='start')
async def start_command_handler(message: types.Message):
    await bot.send_message(message.chat.id,
                           f"Hello {message.from_user.first_name}. This bot is a Planner bot for spbstu students."
                           "\nPress /check_deadlines to do something.")


@bot.message_handler(func=lambda m: True)
async def echo_all(message):
    await bot.reply_to(message, message.text)


@bot.message_handler(commands='check_deadlines')
async def start_command_handler(message: types.Message):
    # get current datetime
    # now = datetime.now()

    # create PostgreSQL cursor object
    conn = await asyncpg.connect(user="postgres", password="0802",
                                 database="lab_manager_database", host="127.0.0.1")

    values = await conn.fetch('''SELECT * FROM users''')
    print(values)
    # execute SQL query to select deadline_id and deadline timestamp from the database
    # execute SQL query to select deadline_id and deadline timestamp from the database
    query = """SELECT specifier, deadline_time, name, tg_chat_id, subject FROM deadlines
               INNER JOIN subjects
                 ON deadlines.subject_id = subjects.plan_id
               INNER JOIN plans
                 ON subjects.plan_id = plans.id
               WHERE deadline_status = True AND extract(hour from timestamp (deadline_time-current_date)) < 24
               ORDER BY tg_chat_id"""
    # combined_message = "\n".join(values)
    await bot.send_message(404247225, values)
    # получает таблицу и отправляет всем кто в ней есть, к тому же если у одного чела три дедлайна завтра
    # отправляет это одним сообщением

    # close database cursor and connection
    await conn.close()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(run())
asyncio.run(bot.polling())
