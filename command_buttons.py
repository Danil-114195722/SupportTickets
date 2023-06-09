from aiogram import types

# Клиентская клавиатура
client_ticket_list_button = types.KeyboardButton('Список тикетов')
client_new_ticket_button = types.KeyboardButton('Новый тикет')
client_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
client_keyboard.add(client_ticket_list_button, client_new_ticket_button)

# Клавиатура для тех. специалистов
technic_ticket_list_button = types.KeyboardButton('Список тикетов')
technic_choose_ticket_button = types.KeyboardButton('Начать сессию')
technic_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
technic_keyboard.add(technic_ticket_list_button, technic_choose_ticket_button)

# определяем клавиатуру для выбора приоритета тикета
priority_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
priority_keyboard.row('Низкий', 'Средний', 'Высокий')

# клавиатура для выхода из сессии обычного пользователя
quit_session_button_regular = types.KeyboardButton('Завершить сессию')
close_ticket_button_regular = types.KeyboardButton('Закрыть тикет')
session_keyboard_regular = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
session_keyboard_regular.add(quit_session_button_regular, close_ticket_button_regular)

# клавиатура для выхода из сессии техника
quit_session_button_technic = types.KeyboardButton('Завершить сессию')
ticket_info_button_technic = types.KeyboardButton('Инфо о тикете')
session_keyboard_technic = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
session_keyboard_technic.add(quit_session_button_technic, ticket_info_button_technic)
