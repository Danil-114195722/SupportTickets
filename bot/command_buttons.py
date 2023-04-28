from aiogram import types

# client keyboard
client_ticket_list_button = types.KeyboardButton('Список тикетов')
client_new_ticket_button = types.KeyboardButton('Новый тикет')
client_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
client_keyboard.add(client_ticket_list_button, client_new_ticket_button)

# keyboard for technician
technic_ticket_list_button = types.KeyboardButton('Список тикетов')
technic_choose_ticket_button = types.KeyboardButton('Выбрать тикет')
technic_keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
technic_keyboard.add(technic_ticket_list_button, technic_choose_ticket_button)
