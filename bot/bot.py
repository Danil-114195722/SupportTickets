from aiogram.utils import executor
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import db_connect as db
from config import TOKEN
from command_buttons import client_keyboard, technic_keyboard


# Создание бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


'''
------------------------------------------------------------
ФУНКЦИЯ СТАРТА БОТА И ОПРЕДЕЛЕНИЯ КЕМ ЯВЛЯЕТСЯ ПОЛЬЗОВАТЕЛЬ
------------------------------------------------------------
'''


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    # Определение пользователя
    user_id = message.from_user.id
    # Проверка, является ли пользователь тех. специалистом
    is_technic = False
    # Добавление пользователя в базу данных, если его там еще нет
    db.add_user(user_id=user_id, username=message.from_user.username, user_status='technic' if is_technic else 'regular')
    # Отправка сообщения пользователю
    if is_technic:
        # Обработчик для тех. специалиста
        await message.answer(f'Добро пожаловать, {message.from_user.username}, вы вошли в режим работника тех.поддержки'
                             f'! Выберите действие:', reply_markup=technic_keyboard)
    else:
        # Обработчик для тех. специалиста
        await message.answer(f'Добро пожаловать, {message.from_user.username}! Выберите действие:', reply_markup=client_keyboard)


'''
---------------------
ФУНКЦИИ ДЛЯ КЛИЕНТОВ
---------------------
'''


# Обработчик для кнопки "Список тикетов" у клиента
@dp.message_handler(text='Список тикетов', user_status='regular')
async def show_ticket_list_handler(message: types.Message):
    # Получение списка тикетов из базы данных
    ticket_list = db.get_ticket_list_regular(user_id=message.from_user.id)
    # Отправка сообщения пользователю со списком тикетов
    await message.answer('\n'.join(ticket_list))


# Обработчик для кнопки "Новый тикет" у клиента
@dp.message_handler(text='Новый тикет', user_status='regular')
async def new_ticket_handler(message: types.Message):
    # Отправка сообщения пользователю с запросом на тему тикета
    await message.answer('Введите тему тикета:')
    # Переход к следующему обработчику
    dp.register_message_handler(new_ticket_priority_handler, user_id=message.from_user.id, user_status='regular')


# Обработчик для приоритета тикета у клиента
async def new_ticket_priority_handler(message: types.Message):
    # Получение выбранного приоритета тикета
    priority = message.text
    # Отправка сообщения пользователю с запросом на описание проблемы
    await message.answer('Опишите проблему:')
    # Добавление тикета в базу данных
    db.add_ticket(user=message.from_user.id, theme=1, message_text=message.text, false_priority=priority)
    # Переход к следующему обработчику
    dp.register_message_handler(new_ticket_finish_handler, user_id=message.from_user.id, user_status='regular')


# Обработчик для завершения создания нового тикета у клиента
async def new_ticket_finish_handler(message: types.Message):
    # Отправка сообщения пользователю о завершении создания тикета
    await message.answer('Тикет успешно создан! Ожидайте ответа.')
    # Переход к начальному обработчику
    dp.register_message_handler(start_handler, commands=['start'])


'''
----------------------------
ФУНКЦИИ ДЛЯ ТЕХ.СПЕЦИАЛИСТОВ
----------------------------
'''


# Обработчик для кнопки "Список тикетов" у тех. специалиста
@dp.message_handler(text='Список тикетов', user_status='technic')
async def show_ticket_list_handler(message: types.Message):
    # получение списка тикетов из базы данных
    ticket_list = db.get_ticket_list_technic()
    # отправка сообщения пользователю со списком тикетов
    await message.answer('\n'.join(ticket_list))


# Обработчик для кнопки "Выбрать тикет" у тех. специалиста
@dp.message_handler(text='Выбрать тикет', userstatus='technic')
async def choose_ticket_handler(message: types.Message):
    # отправка сообщения пользователю с запросом на выбор тикета
    await message.answer('Выберите тикет:')
    # переход к следующему обработчику
    dp.register_message_handler(technic_ticket_info_handler, user_id=message.from_user.id, user_status='technic')


# Обработчик для информации о тикете у тех. специалиста
async def technic_ticket_info_handler(message: types.Message):
    # Получение информации о тикете из базы данных
    ticket_info = db.get_ticket_info_technic(ticket_id=message.text)
    # Отправка сообщения пользователю с информацией о тикете
    await message.answer(ticket_info)
    # Добавление кнопки "Начать сессию"
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Начать сессию'))
    await message.answer('Нажмите кнопку "Начать сессию", чтобы начать общение с клиентом.', reply_markup=keyboard)
    # Переход к следующему обработчику
    dp.register_message_handler(technic_ticket_info_handler, user_id=message.from_user.id, user_status='technic')


# Обработчик для сессии у тех. специалиста
async def technic_session_handler(message: types.Message):
    # Отправка сообщения клиенту через-бота
    await bot.send_message(chat_id=message.text, text='Вы начали сессию с тех.специалистом! Можете задавать вопросы.')
    # Добавление кнопки "Закончить сессию"
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Закончить сессию'))
    await message.answer('Нажмите кнопку "Закончить сессию", чтобы завершить общение.', reply_markup=keyboard)
    # Переход к следующему обработчику
    dp.register_message_handler(technic_feedback_handler, user_id=message.from_user.id, user_status='technic')


# Обработчик для отзыва о работе тех. специалиста у клиента
async def technic_feedback_handler(message: types.Message):
    # Отправка сообщения клиенту с просьбой об оставлении отзыва
    await bot.send_message(chat_id=message.text, text='Оцените работу тех.специалиста!')
    # Переход к начальному обработчику
    dp.register_message_handler(start_handler, commands=['start'])


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
