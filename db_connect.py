import mysql.connector
from mysql.connector.errors import Error as MySQLError

from config import DB_USER_PASS


# делаем соединение с БД
CONNECTION = mysql.connector.connect(
    host='79.137.204.172',
    port='3306',
    user='support_user',
    passwd=DB_USER_PASS,
    database='support_db'
)


# выполнение SQL запроса без отдачи
def exec_query_without_resp(query: str) -> None:
    with CONNECTION.cursor() as cur:
        # выполняем SQL запрос
        try:
            cur.execute(query)
            CONNECTION.commit()
            print('Query OK')
        # если произошла ошибка
        except MySQLError as error:
            print(f'You got error in file "db_connection.py": {error}')


# выполнение SQL запроса с отдачей
def exec_query_with_resp(query: str) -> tuple:
    gotten_info = tuple()

    with CONNECTION.cursor() as cur:
        # выполняем SQL запрос
        try:
            cur.execute(query)
            gotten_info = cur.fetchall()
            print('Query OK')
        # если произошла ошибка
        except MySQLError as error:
            print(f'You got error in file "db_connection.py": {error}')

    return gotten_info


# добавление пользователя
def add_user(user_id: int, username: str = 'клиент', user_status: str = 'regular') -> None:
    add_query = f'''INSERT INTO user (user_id, username, user_status) VALUES
    ("{user_id}", "{username}", "{user_status}")'''
    # выполняем SQL запрос
    exec_query_without_resp(query=add_query)


# добавление тикета
def add_ticket(user: int, theme: str, message_text: str, false_priority: str = '0') -> None:
    add_query = f'''INSERT INTO ticket (user, theme, message_text, false_priority) VALUES
    ("{user}", "{theme}", "{message_text}", "{false_priority}")'''
    # выполняем SQL запрос
    exec_query_without_resp(query=add_query)


# получение всей инфы о пользователе по id пользователя в тг
def get_table_id_user(user_id: int) -> tuple:
    get_query = f'''SELECT * FROM user  WHERE user_id = {user_id};'''
    # выполняем SQL запрос и возвращаем его ответ
    table_id_user = exec_query_with_resp(query=get_query)[0]
    return table_id_user


# закрыть задачу (поставить в значение done 1)
def close_ticket(ticket_id: int) -> None:
    update_query = f'''UPDATE ticket SET ticket.done = 1 WHERE ticket.id = {ticket_id}'''
    # выполняем SQL запрос
    exec_query_without_resp(query=update_query)


# вывод всех тикетов определённого пользователя
def get_ticket_list_regular(user_id: int) -> tuple:
    get_query = f'''SELECT ticket.theme, ticket.message_text, ticket.false_priority, ticket.true_priority, ticket.done
    FROM ticket INNER JOIN user ON ticket.user = user.id
    WHERE user_id = {user_id};'''
    # выполняем SQL запрос и возвращаем его ответ
    ticket_list_regular = exec_query_with_resp(query=get_query)
    return ticket_list_regular


# вывод всех нерешённых тикетов
def get_ticket_list_technic() -> tuple:
    get_query = f'''SELECT user.user_id, ticket.id, ticket.theme, ticket.false_priority, ticket.true_priority
    FROM ticket INNER JOIN user ON ticket.user = user.id
    WHERE ticket.done = 0;'''
    # выполняем SQL запрос и возвращаем его ответ
    ticket_list_technic = exec_query_with_resp(query=get_query)
    return ticket_list_technic


# вывод полной информации об одном тикете по его id
def get_ticket_info_technic(ticket_id: int) -> tuple:
    get_query = f'''SELECT ticket.id, user.user_id, user.username, ticket.theme, ticket.message_text, ticket.false_priority, ticket.done
    FROM ticket INNER JOIN user ON ticket.user = user.id
    WHERE ticket.id = {ticket_id};'''
    # выполняем SQL запрос и возвращаем его ответ
    ticket_info_technic = exec_query_with_resp(query=get_query)
    return ticket_info_technic


if __name__ == '__main__':
    pass
    # add_user(user_id=123456, username='Алексей', user_status='technic')
    # add_theme(name='server issues')
    # add_ticket(user=16, theme='server issfgsue', message_text="I've got dfgdg problem. Can you help me? It's emergency!!!", false_priority=1)
    # print(get_ticket_list_regular(user_id=123456))
    # print('-------------------------------------')
    # print(get_ticket_info_technic(ticket_id=1))
    # print('-------------------------------------')
    # list_tickets = get_ticket_list_technic()[0]
    # print(list_tickets)
    # print(str(list_tickets[3]))
    # print('-------------------------------------')
    # print(get_table_id_user(user_id=123456))
    # print('-------------------------------------')
    # print(get_ticket_list_technic())
