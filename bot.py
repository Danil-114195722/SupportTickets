from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext, filters
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ChatMember, ContentTypes

from re import match
import db_connect as db
from config import TOKEN
from command_buttons import client_keyboard, technic_keyboard, priority_keyboard

# Создание бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

INPUT_PRIORITY = {
    'Низкий': '0',
    'Средний': '1',
    'Высокий': '2',
}

OUTPUT_PRIORITY = {
    '0': 'Низкий',
    '1': 'Средний',
    '2': 'Высокий',
}

COMPLETED = {
    0: 'в ожидании ответа',
    1: 'завершён',
}


class StatusRegular(StatesGroup):
    regular_id = None

    regular = State()
    theme_ticket = State()
    priority = State()
    add_ticket = State()
    waiting_for_technic = State()
    regular_msg = State()


class StatusTechnic(StatesGroup):
    technic_id = None

    technic = State()
    waiting_for_client = State()
    technic_msg = State()


class QAN(StatesGroup):
    technic_id = None
    technic_table_id = None
    select_chat_id = State()
    connection = State()


# class StatusSession(StatesGroup):
#     session = State()
#
#
# class Chatting(StatesGroup):
#     regular_id = None
#     technic_id = None
#     msg = State()


'''
-----------------------------------------------------------
ФУНКЦИЯ СТАРТА БОТА И ОПРЕДЕЛЕНИЯ КЕМ ЯВЛЯЕТСЯ ПОЛЬЗОВАТЕЛЬ
-----------------------------------------------------------
'''


@dp.message_handler(commands=['start'], state="*")
async def start_handler(message: types.Message, state: FSMContext):
    # Определение пользователя
    user_id = message.from_user.id
    # Проверка, является ли пользователь тех. специалистом
    is_technic = True
    # получаем инфо о пользователе
    try:
        user_info = db.get_table_id_user(user_id=user_id)
    # выдаёт ошибку, если его там нет, поэтому добавляем пользователя в базу данных
    except IndexError:
        db.add_user(user_id=user_id, username=message.from_user.first_name,
                    user_status='technic' if is_technic else 'regular')
        user_info = db.get_table_id_user(user_id=user_id)

    if user_info[-1] == 'technic':
        await message.answer(f'Добро пожаловать, {message.from_user.first_name}, вы вошли в режим работника тех.поддержки!', reply_markup=technic_keyboard)
        await StatusTechnic.technic.set()
    else:
        await message.answer(f'Добро пожаловать, {message.from_user.first_name}!', reply_markup=client_keyboard)
        await StatusRegular.regular.set()


'''
--------------------
ФУНКЦИИ ДЛЯ КЛИЕНТОВ
--------------------
'''


# Обработчик для кнопки "Список тикетов" у клиента
@dp.message_handler(text='Список тикетов', state=StatusRegular.regular)
async def ticket_list_handler(message: types.Message):
    # Отправляем список тикетов пользователю
    response = ''
    for ticket in db.get_ticket_list_regular(user_id=message.from_user.id):
        # print(ticket)
        ticket_text = f'''Theme: {ticket[0]}\nMessage: {ticket[1]}\nFalse Priority: {OUTPUT_PRIORITY.get(ticket[2])}
        Create Datatime: {ticket[3]}\nCompleted: {COMPLETED.get(ticket[4])}\n\n'''
        response += ticket_text
        print(ticket_text)
    if response:
        await message.answer(response)
    else:
        await message.answer('У вас нет тикетов')


# Обработчик для кнопки "Новый тикет" у клиента
@dp.message_handler(text='Новый тикет', state=StatusRegular.regular)
async def new_ticket_handler(message: types.Message, state: FSMContext):
    # Отправка сообщения пользователю с запросом на тему тикета
    await message.answer('Введите тему тикета:')
    # Переходим в следующий статус
    await StatusRegular.theme_ticket.set()


# Обработчик для выбора темы тикета у клиента
@dp.message_handler(state=StatusRegular.theme_ticket)
async def ticket_theme_handler(message: types.Message, state: FSMContext):
    # Сохраняем тему тикета в контексте
    await state.update_data(theme=message.text)
    # Отправляем сообщение с запросом на приоритет тикета
    await message.answer('Выберите приоритет тикета:', reply_markup=priority_keyboard)
    # Переходим в следующий статус
    await StatusRegular.priority.set()


# Обработчик для выбора приоритета тикета у клиента
@dp.message_handler(lambda message: message.text in ['Низкий', 'Средний', 'Высокий'], state=StatusRegular.priority)
async def ticket_priority_handler(message: types.Message, state: FSMContext):
    # Сохраняем приоритет тикета в контексте
    await state.update_data(priority=message.text)
    # Отправляем сообщение с запросом на описание проблемы
    await message.answer('Опишите вашу проблему:', reply_markup=ReplyKeyboardRemove())
    # Переходим в следующий статус
    await StatusRegular.add_ticket.set()


# Обработчик для создания нового тикета у клиента
@dp.message_handler(state=StatusRegular.add_ticket)
async def create_ticket_handler(message: types.Message, state: FSMContext):
    # Получаем данные из контекста
    data = await state.get_data()
    theme = data.get('theme')
    priority = data.get('priority')
    description = message.text
    # Добавляем тикет в базу данных
    table_id_user = db.get_table_id_user(user_id=message.from_user.id)[0]
    db.add_ticket(user=table_id_user, theme=theme, message_text=description, false_priority=INPUT_PRIORITY.get(priority))
    # Отправляем сообщение пользователю
    await message.answer('Ваш тикет успешно создан!')
    # Возвращаемся в начальный статус
    await StatusRegular.regular.set()


'''
----------------------------
ФУНКЦИИ ДЛЯ ТЕХ.СПЕЦИАЛИСТОВ
----------------------------
'''


# Обработчик для кнопки "Список тикетов" у тех. специалиста
@dp.message_handler(text='Список тикетов', state=StatusTechnic.technic)
async def technic_ticket_list_handler(message: types.Message):
    # Отправляем список всех тикетов
    # формируем сообщение с информацией о тикетах
    response = ''
    for ticket in db.get_ticket_list_technic():
        # print(ticket)
        ticket_text = f'''User ID: {ticket[0]}\nTicket ID: {ticket[1]}\nTheme: {ticket[2]}
False Priority: {OUTPUT_PRIORITY.get(ticket[3])}\nCreate Datatime: {ticket[4]}\n\n'''
        response += ticket_text
        print(ticket_text)
    # отправляем сообщение с информацией о тикетах
    await message.answer(response)


# Обработчик кнопки "Начать сессию" у тех. специалиста
@dp.message_handler(text='Начать сессию', state=StatusTechnic.technic)
async def start_session(message: types.Message, state: FSMContext):
    # Сохраняем ID тех. специалиста в контексте
    await state.update_data(technic_id=message.from_user.id)
    # Отправляем сообщение пользователю с запросом ID клиента
    await message.answer('Введите ID клиента:')
    # Переходим в статус waiting_for_client
    await StatusTechnic.waiting_for_client.set()


'''
--------------
ФУНКЦИИ СЕССИИ
--------------
'''


# Обработчик ответа клиента на запрос ID у тех. специалиста
@dp.message_handler(state=StatusTechnic.waiting_for_client)
async def waiting_for_client(message: types.Message, state: FSMContext):
    # Получаем ID клиента из сообщения
    client_id = int(message.text)
    # получаем имя клиента из БД
    client_name = db.get_table_id_user(user_id=client_id)[2]
    # Сохраняем ID клиента в контексте
    await state.update_data(client_id=client_id)
    # Отправляем сообщение тех. специалисту с информацией о клиенте
    await message.answer(f'Идёт подключение с клиентом ID: {client_id} Name: {client_name}')
    # print(StatusTechnic.technic_id)

    data = await state.get_data()
    technic_id = data.get('technic_id')
    print(technic_id)

    technic_table_id = str(db.get_table_id_user(user_id=technic_id)[0]).rjust(3, '0')
    await bot.send_message(chat_id=client_id,
                           text=f'Тех.специалист {technic_table_id} готов начать чать, нажмите на /start_session_{technic_table_id} чтобы начать чат')
    # Переходим в статус
    await StatusRegular.waiting_for_technic.set()
    # await StatusRegular.regular_msg.set()


# Обработчик ответа тех. специалиста на запрос ID клиента
@dp.message_handler(state=StatusRegular.waiting_for_technic)
async def waiting_for_technic(message: types.Message, state: FSMContext):
    # Получаем ID тех. специалиста и клиента из контекста
    data = await state.get_data()
    technic_id = data.get('technic_id')
    client_id = data.get('client_id')
    # Отправляем сообщение клиенту с запросом на начало сессии
    button_1 = KeyboardButton('Да')
    button_2 = KeyboardButton("Нет")
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(button_1, button_2)
    await bot.send_message(chat_id=client_id,
                           text=f'Тех.специалист {db.get_table_id_user(user_id=technic_id)[2]} хочет начать сессию. Присоединиться?',
                           reply_markup=keyboard)
    # Переходим в статус SESSION
    # await StatusSession.session.set()
    StatusTechnic.regular_id = client_id
    StatusTechnic.technic_id = technic_id
    await StatusTechnic.technic_msg.set()


# # Обработчик ответа клиента на запрос на начало сессии
# @dp.message_handler(commands=['Да'], state=StatusSession.session)
# async def start_session_handler(message: types.Message, state: FSMContext):
#     # Получаем ID тех. специалиста и клиента из контекста
#     data = await state.get_data()
#     technic_id = data.get('technic_id')
#     client_id = data.get('client_id')
#     # Отправляем сообщение тех. специалисту о начале сессии
#     await bot.send_message(chat_id=technic_id, text=f'Клиент {client_id} согласен на начало сессии.', reply_markup=ReplyKeyboardRemove)
#     await Chatting.msg.set()
#
#
# # Обработчик ответа клиента на запрос на начало сессии
# @dp.message_handler(commands=['Нет'], state=StatusSession.session)
# async def cancel_session_handler(message: types.Message, state: FSMContext):
#     # Получаем ID тех. специалиста и клиента из контекста
#     data = await state.get_data()
#     technic_id = data.get('technic_id')
#     client_id = data.get('client_id')
#     # Отправляем сообщение тех. специалисту об отмене сессии
#     await bot.send_message(chat_id=technic_id, text=f'Клиент {client_id} отказался от начала сессии.', reply_markup=ReplyKeyboardRemove)
#     # Переходим в начальный статус
#     await state.finish()


# @dp.message_handler(commands=['cancel'])
# @dp.message_handler(state=[StatusTechnic.technic_msg, StatusRegular.regular_msg])
# async def chatting_technic(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer('Жмите /start')


@dp.message_handler(content_types=ContentTypes.TEXT)
@dp.message_handler(state=QAN.select_chat_id)
async def chatting_client(message: types.Message, state: FSMContext):
    await state.update_data(msg=message.text)
    user_data = await state.get_data()
    technic_id = StatusTechnic.technic_id
    await bot.send_message(technic_id, user_data['msg'])


# @dp.message_handler(content_types=ContentTypes.TEXT)
# @dp.message_handler(state=StatusTechnic.technic_msg)
# async def chatting_technic(message: types.Message, state: FSMContext):
#     await state.update_data(msg=message.text)
#     user_data = await state.get_data()
#     client_id = StatusRegular.regular_id
#     await bot.send_message(client_id, user_data['msg'])
#
#
# @dp.message_handler(content_types=ContentTypes.TEXT)
# @dp.message_handler(state=StatusRegular.regular_msg)
# async def chatting_client(message: types.Message, state: FSMContext):
#     await state.update_data(msg=message.text)
#     user_data = await state.get_data()
#     technic_id = StatusTechnic.technic_id
#     await bot.send_message(technic_id, user_data['msg'])


# @dp.message_handler(content_types=ContentTypes.TEXT)
# @dp.message_handler(state=Chatting.msg)
# async def chatting_technic(message: types.Message, state: FSMContext):
#     await state.update_data(msg=message.text)
#     user_data = await state.get_data()
#     client_id = Chatting.regular_id
#     await bot.send_message(client_id, user_data['msg'])
#
# @dp.message_handler(content_types=ContentTypes.TEXT)
# @dp.message_handler(state=Chatting.msg)
# async def chatting_client(message: types.Message, state: FSMContext):
#     await state.update_data(msg=message.text)
#     user_data = await state.get_data()
#     technic_id = Chatting.technic_id
#     await bot.send_message(technic_id, user_data['msg'])


@dp.message_handler()
async def change_user_state(message: types.Message):
    message_text = message.text
    if match('^/start_session_\d{3}', message_text):
        technic_table_id = int(message_text.split('_')[-1])
        technic_user_id = db.get_user_id(table_id=technic_table_id)
        QAN.technic_id = technic_user_id
        QAN.technic_table_id = technic_table_id
        await QAN.select_chat_id.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
