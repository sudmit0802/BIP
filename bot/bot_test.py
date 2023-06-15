import asyncio
import asyncpg
from telebot.async_telebot import AsyncTeleBot
from telebot import types, asyncio_filters
import random
import datetime
import string
from smtplib import SMTP
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage

bot = AsyncTeleBot(token='6236134779:AAF9IVmzQl2vAz9e5U8BCG8bqGECE_RzSUw', state_storage=StateMemoryStorage())

# Generate authentication code
async def generate_code():
    code = ''
    for i in range(6):
        code += str(random.randrange(10))
    return code


async def connect_db():
    return await asyncpg.connect(user="postgres", password="0802",
                                    database="lab_manager_database", host="127.0.0.1")


async def send_email(message, reciever):
    sender = "denisnepovis@mail.ru"
    password = "d5pVbceLH1pnpwzNn3ay"
    server = SMTP("smtp.mail.ru", 587)
    server.ehlo()
    server.starttls()
    server.login(sender, password)
    try:
        server.sendmail(sender, reciever, message)
    except Exception as e:
        print(e)
        await bot.send_message(reciever, "Error: Failed to send email.")
    server.quit()

# Just create different statesgroup
class MyStates(StatesGroup):
    is_authenticated = State() # statesgroup should contain states
    new_guest = State() # statesgroup should contain states
    email = State() # statesgroup should contain states
    auth_code_recv = State()

# set_state -> sets a new state
# delete_state -> delets state if exists
# get_state -> returns state if exists
LOG = True

# Start command handler
@bot.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    await check_authenticated(message)

     
async def check_authenticated(message):
    conn = await connect_db()
    values = await conn.fetch(f"""select tg_chat_id from users WHERE tg_chat_id = '{message.chat.id}'""")
    print(f"""select tg_chat_id from users WHERE tg_chat_id = '{message.chat.id}'""")
    print(values) # DELETE
    await conn.close()

    if not values:
        # values is an empty list
        #пользователь не пользовался тг-ботом
        await bot.set_state(message.from_user.id, MyStates.new_guest, message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        auth_button = types.KeyboardButton('🦄 Пройти аутентификацию 🦄')
        markup.add(auth_button)
        await bot.send_message(message.chat.id, "Привет! Пожалуйста, пройди аутентификацию.", reply_markup=markup)
    else:
        await bot.set_state(message.from_user.id, MyStates.is_authenticated, message.chat.id)
        # добавляем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        auth_button = types.KeyboardButton('🌊 Меню 🌊')
        markup.add(auth_button)
        await bot.send_message(message.chat.id, "Привет, {}! Мы уже знакомы, переходи в меню:".format(message.from_user.username), reply_markup=markup)    

# Authorization button handler
@bot.message_handler(func=lambda message: message.text == '🦄 Пройти аутентификацию 🦄')
async def auth_button_handler(message: types.Message):
    state = await bot.get_state(message.chat.id)
    #print(state)
    if state == 'MyStates:new_guest':
        #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup = types.ReplyKeyboardRemove()
        #markup.add(types.KeyboardButton(text="Отправить код аутентификации"))
        await bot.set_state(message.from_user.id, MyStates.email, message.chat.id)
        await bot.send_message(message.chat.id, "Введите свой email для аутентификации.", reply_markup=markup)



# Menu button handler
@bot.message_handler(func=lambda message: message.text == '🌊 Меню 🌊')
async def auth_button_handler(message: types.Message):
    state = await bot.get_state(message.chat.id)
    print(state)
    if state == 'MyStates:is_authenticated':
        markup = types.ReplyKeyboardMarkup()
        button_plans = types.KeyboardButton('мои планы')
        close_deadlines = types.KeyboardButton('список ближайших дедлайнов')
        button_report = types.KeyboardButton('отчет')
        markup.row(button_plans)
        markup.row(close_deadlines)
        markup.row(button_report)
        await bot.send_message(message.chat.id, "Выбери кнопку:", reply_markup=markup)

    else:
        print('not is_authenticated')
        await check_authenticated(message) 



@bot.message_handler(func=lambda message: message.text == 'мои планы')
async def auth_button_handler(message: types.Message):
    state = await bot.get_state(message.chat.id)
    print(state)
    if state == 'MyStates:is_authenticated':
        await get_plans_from_db(message)
    else:
        print('not is_authenticated')
        await check_authenticated(message) 


async def get_plans_from_db(message):
    conn = await connect_db()
    values = await conn.fetch(f"""select\
    subjects.name, plans.name, users.username, deadlines.deadline_time, plans.status, deadlines.specifier, deadlines.deadline_status\
    from users\
    join plans\
    on plans.user_id = users.id\
    join subjects\
    on subjects.plan_id = plans.id\
    join deadlines\
    on subjects.id = deadlines.subject_id\
    where users.tg_chat_id = '{message.chat.id}'\
    order by plans.name, deadline_time""")
    #print(values) # DELETE 
    await conn.close()

    if not values:
        # values is an empty list
        # добавляем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        auth_button = types.KeyboardButton('🌊 Меню 🌊')
        markup.add(auth_button)
        await bot.send_message(message.chat.id, "Кажется у вас нет созданных планов", reply_markup=markup)
    else:
        await bot.set_state(message.from_user.id, MyStates.is_authenticated, message.chat.id)
        # добавляем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        auth_button = types.KeyboardButton('🌊 Меню 🌊')
        markup.add(auth_button)
        plans = ""
        print(values)
        deadline_status = ""
        for i, record in enumerate(values):
            if record[6] == True:
                deadline_status = "active"
            else:
                deadline_status = "inactive"
            if i == 0 or values[i][1]!=values[i-1][1]:
                plans += f"{i+1}.📌 План: {record[1]}, статус: {record[4]} \n"
            plans += f"🎯Дедлайн: {record[5]}, статус: {deadline_status}\n🎓Предмет: {record[0]}\n⏳Дата: {record[3]}\n"
            plans += "--------------------------------------------\n"
        await bot.send_message(message.chat.id, plans, reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'список ближайших дедлайнов')
async def auth_button_handler(message: types.Message):
    state = await bot.get_state(message.chat.id)
    print(state)
    if state == 'MyStates:is_authenticated':
        await get_soon_deadlines(message)
    else:
        print('not is_authenticated')
        await check_authenticated(message) 


async def get_soon_deadlines(message):
    conn = await connect_db()
    values = await conn.fetch(f"""select\
    subjects.name, plans.name, users.username, deadlines.deadline_time\
    from users\
    join plans\
    on plans.user_id = users.id\
    join subjects\
    on subjects.plan_id = plans.id\
    join deadlines\
    on subjects.id = deadlines.subject_id\
    where users.tg_chat_id = '{message.chat.id}' and plans.status = 'active' and deadline_status = True\
    order by deadline_time\
    limit 5""")
    print(values) # DELETE 
    await conn.close()

    if not values:
        # values is an empty list
        # добавляем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        auth_button = types.KeyboardButton('🌊 Меню 🌊')
        markup.add(auth_button)
        await bot.send_message(message.chat.id, "Ничего не нашли", reply_markup=markup)
    else:
        await bot.set_state(message.from_user.id, MyStates.is_authenticated, message.chat.id)
        # добавляем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        auth_button = types.KeyboardButton('🌊 Меню 🌊')
        markup.add(auth_button)
        deadlines = ""
        for i, recordww in enumerate(values):
           deadlines += f"{i+1}. --------------------------------------------\n🎓Предмет: {recordww[0]}\n⏳Дата: {recordww[3]}\n📌План: {recordww[1]}\n"

        await bot.send_message(message.chat.id, deadlines, reply_markup=markup)


@bot.message_handler(state="*", commands='cancel')
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Отмена")
    await bot.delete_state(message.from_user.id, message.chat.id)


@bot.message_handler(state=MyStates.email)
async def name_get(message):
    """
    State 1. Will process when user's state is MyStates.email.
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['email'] = message.text
        #проверить, что у нас есть зарегистрированный на сайте пользователь с данной почтой
        conn = await connect_db()
        values = await conn.fetch(f"""SELECT email FROM users WHERE email = '{data['email']}'""")
        await conn.close()

        if not values:
            # values is an empty list
            #пользователь с такой почтой не регистрировался на сайте(
            await bot.delete_state(message.from_user.id, message.chat.id)  #!!!! проверить корректность работы
            await bot.set_state(message.from_user.id, MyStates.new_guest, message.chat.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            auth_button = types.KeyboardButton('🦄 Пройти аутентификацию 🦄')
            markup.add(auth_button)
            await bot.send_message(message.chat.id, f'Ой, кажется эта почта нам неизвестна. Используйте почту, указанную при регистрации на сайте. Либо зарегистрируйтесь, если вы не делали этого ранее.', reply_markup=markup)
        else:
            auth_code = await generate_code()
            data['auth_code_sent'] = auth_code
            msg = 'One-Time Password for Sign In: ' + auth_code
            await send_email(msg, message.text)
            await bot.send_message(message.chat.id, f'Спасибо, мы отправили вам код аутентификации на почту. Ведите его:')
            await bot.set_state(message.from_user.id, MyStates.auth_code_recv, message.chat.id)

@bot.message_handler(state=MyStates.auth_code_recv)
async def name_get(message):
    """
    State 2. Will process when user's state is MyStates.auth_code_recv.
    """
    async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['auth_code_recv'] = message.text
        if data['auth_code_sent'] == data['auth_code_recv']:
            #пытаемся внести tg_chat_id пользователя в бд
            conn = await connect_db()
            values = await conn.fetch(f"""UPDATE users SET tg_chat_id = '{message.chat.id}' WHERE email = '{data['email']}'""")
            await conn.close() 
            print(values) # DELETE

            if values == 'UPDATE 0':
            #пользователь с такой почтой не регистрировался на сайте(
                await bot.send_message(message.chat.id, f'Ой, кажется эта почта нам неизвестна. Используйте почту, указанную при регистрации на сайте. Либо зарегистрируйтесь, если вы не делали этого ранее.')
                await bot.delete_state(message.from_user.id, message.chat.id)
                await bot.set_state(message.from_user.id, MyStates.new_guest, message.chat.id)
            
            await bot.set_state(message.from_user.id, MyStates.is_authenticated, message.chat.id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            auth_button = types.KeyboardButton('🌊 Меню 🌊')
            markup.add(auth_button)
            await bot.send_message(message.chat.id, f'Отлично, вы прошли аутентификацию, теперь перейдите в меню, чтобы увидеть доступные функции', reply_markup=markup)
        else:
            #введеный код не совпал с отправленным
            await bot.send_message(message.chat.id, "Ошибка аутентификации. Проверьте правильность введенного кода и email.")
            await bot.delete_state(message.from_user.id, message.chat.id)
            await bot.set_state(message.from_user.id, MyStates.new_guest, message.chat.id)


async def check_deadlines_every_evening():
    conn = await connect_db()
    values = await conn.fetch(f"""select\
    subjects.name, plans.name, users.username, deadlines.deadline_time\
    from users\
    join plans\
    on plans.user_id = users.id\
    join subjects\
    on subjects.plan_id = plans.id\
    join deadlines\
    on subjects.id = deadlines.subject_id\
    where users.tg_chat_id = '{message.chat.id}' and plans.status = 'active' and deadline_status = True\
    order by deadline_time\
    limit 5""")
    print(values) # DELETE 
    await conn.close()
    print('Отправлено сообщение!')

# Функция, выполняющая проверку времени и вызывающая функцию отправки сообщения
async def check_time_and_send():
    while True:
        current_time = datetime.datetime.now().time()
        
        if current_time >= datetime.time(11, 0) and current_time <= datetime.time(12, 0):
        #if current_time >= datetime.time(19, 0) and current_time <= datetime.time(20, 0):
            await check_deadlines_every_evening()
        await asyncio.sleep(6 * 60)  # Проверяем время каждые n * 60 



async def run():
    while True:
        conn = await connect_db()
        values = await conn.fetch("""select * from users""")
        await bot.send_message(404247225, values)
        await conn.close()
        await asyncio.sleep(3600)


async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.create_task(check_time_and_send())
    await asyncio.sleep(1)
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main())