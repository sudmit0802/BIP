import asyncio
import asyncpg
from telebot.async_telebot import AsyncTeleBot
from telebot import types, asyncio_filters
import random
import string
from smtplib import SMTP
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage

bot = AsyncTeleBot(token='6236134779:AAF9IVmzQl2vAz9e5U8BCG8bqGECE_RzSUw', state_storage=StateMemoryStorage())

# Generate authentication code
def generate_code(length):
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(length))


# Just create different statesgroup
class MyStates(StatesGroup):
    is_authenticated = State() # statesgroup should contain states
    new_guest = State() # statesgroup should contain states
    email = State() # statesgroup should contain states
    auth_code_recv = State()

# set_state -> sets a new state
# delete_state -> delets state if exists
# get_state -> returns state if exists


# Start command handler
@bot.message_handler(commands=['start'])
#сразу должна быть проверка, аутентифицировался ли чел уже через тг
# проверка для пользователя с таким  
# вынести функции обращения к бд в отдельный файл
async def start_command_handler(message: types.Message):
    
    conn = await asyncpg.connect(user="postgres", password="0802",
                                    database="lab_manager_database", host="127.0.0.1")
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
        markup = types.ReplyMarkupRemove()
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
        button_create_plan = types.KeyboardButton('создать план')
        button_report = types.KeyboardButton('отчет')
        markup.row(button_plans)
        markup.row(button_create_plan)
        markup.row(button_report)
        await bot.send_message(message.chat.id, "Выбери кнопку:", reply_markup=markup)

    else:
        print('not is_authenticated')        

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
        conn = await asyncpg.connect(user="postgres", password="0802",
                                    database="lab_manager_database", host="127.0.0.1")
        values = await conn.fetch(f"""SELECT email FROM users WHERE email = '{data['email']}'""")
        await conn.close()
        print(values) # DELETE 

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
            print(message.text)  # DELETE 
            mess = generate_code(6)
            print(mess)  # DELETE 
            data['auth_code_sent'] = mess
            await send_email(mess, message.text)
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
            conn = await asyncpg.connect(user="postgres", password="0802",
                                        database="lab_manager_database", host="127.0.0.1")
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


async def run():
    while True:
        conn = await asyncpg.connect(user="postgres", password="0802",
                                     database="lab_manager_database", host="127.0.0.1")
        values = await conn.fetch("""select * from users""")
        await bot.send_message(404247225, values)
        await conn.close()
        await asyncio.sleep(360)


async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    asyncio.create_task(run())
    await asyncio.sleep(1)
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main())