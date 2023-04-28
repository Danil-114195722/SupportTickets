from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import db_connect as db
from config import TOKEN
from aiogram.utils import executor
from command_buttons import client_keyboard, technic_keyboard

# creating a bot
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # user definition
    user_id = message.from_user.id
    # checking if the user is a technician
    # here you can use your own logic to define
    is_technic = False
    # adding a user to the database if it is not already there
    db.add_user(user_id=user_id, username=message.from_user.username, user_status='technic' if is_technic else 'regular')
    # send message to user
    if is_technic:
        # processor for technical specialist
        await message.answer('Добро пожаловать, тех.специалист! Выберите действие:', reply_markup=technic_keyboard)
    else:
        # client handler
        await message.answer('Добро пожаловать, клиент! Выберите действие:', reply_markup=client_keyboard)


# handler for the "List of tickets" button on the client
@dp.message_handler(text='Список тикетов', user_id=USER_ID, user_status='regular')
async def show_ticket_list_handler(message: types.Message):
    # getting a list of tickets from the database
    ticket_list = db.get_ticket_list(user_id=message.from_user.id)
    # sending a message to a user with a list of tickets
    await message.answer('\n'.join(ticket_list))


# handler for the "New ticket" button on the client
@dp.message_handler(text='Новый тикет', user_id=USER_ID, user_status='regular')
async def new_ticket_handler(message: types.Message):
    # send a message to the user asking for the subject of the ticket
    await message.answer('Введите тему тикета:')
    # move to the next handler
    dp.register_message_handler(new_ticket_priority_handler, user_id=message.from_user.id, user_status='regular')


# handler for the priority of the ticket from the client
async def new_ticket_priority_handler(message: types.Message):
    # get selected ticket priority
    priority = message.text
    # sending a message to the user asking for a description of the problem
    await message.answer('Опишите проблему:')
    # adding a ticket to the database
    db.add_ticket(user=message.from_user.id, theme=1, message_text=message.text, false_priority=priority)
    # move to the next handler
    dp.register_message_handler(new_ticket_finish_handler, user_id=message.from_user.id, user_status='regular')


# handler to complete the creation of a new ticket at the client
async def new_ticket_finish_handler(message: types.Message):
    # sending a message to the user about the completion of the creation of the ticket
    await message.answer('Тикет успешно создан! Ожидайте ответа.')
    # jump to start handler
    dp.register_message_handler(start_handler, commands=['start'])


# handler for the "List of tickets" button for a technical specialist
@dp.message_handler(text='Список тикетов', userid=USER_ID, userstatus='technic')
async def show_ticket_list_handler(message: types.Message):
    # getting a list of tickets from the database
    ticket_list = db.get_ticket_list()
    # sending a message to a user with a list of tickets
    await message.answer('\n'.join(ticket_list))


# handler for the "Select ticket" button from a technical specialist
@dp.message_handler(text='Выбрать тикет', userid=USER_ID, userstatus='technic')
async def choose_ticket_handler(message: types.Message):
    # sending a message to the user asking them to select a ticket
    await message.answer('Выберите тикет:')
    # move to the next handler
    dp.register_message_handler(technic_ticket_info_handler, userid=message.from_user.id, userstatus='technic')


# handler for information about a ticket from a technical specialist
async def technic_ticket_info_handler(message: types.Message):
    # getting information about a ticket from the database
    ticket_info = db.get_ticket_info(ticketid=message.text)
    # sending a message to the user with information about the ticket
    await message.answer(ticket_info)
    # adding a button "Start session"
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Начать сессию'))
    await message.answer('Нажмите кнопку "Начать сессию", чтобы начать общение с клиентом.', reply_markup=keyboard)
    # move to the next handler
    dp.register_message_handler(technic_ticket_info_handler, userid=message.from_user.id, userstatus='technic')


# handler for the session at the tech.specialist
async def technic_session_handler(message: types.Message):
    # sending a message to a client via a bot
    await bot.send_message(chat_id=message.text, text='Вы начали сессию с тех.специалистом! Можете задавать вопросы.')
    # adding "End Session" button
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Закончить сессию'))
    await message.answer('Нажмите кнопку "Закончить сессию", чтобы завершить общение.', reply_markup=keyboard)
    # move to the next handler
    dp.register_message_handler(technic_feedback_handler, userid=message.from_user.id, userstatus='technic')


# processor for feedback on the work of a technical specialist at the client
async def technic_feedback_handler(message: types.Message):
    # sending a message to the client asking for feedback
    await bot.send_message(chat_id=message.text, text='Оцените работу тех.специалиста!')
    # jump to start handler
    dp.register_message_handler(start_handler, commands=['start'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)