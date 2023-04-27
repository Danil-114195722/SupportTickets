import mysql.connector
from mysql.connector.errors import Error as MySQLError

from config import DB_USER_PASS


CONNECTION = mysql.connector.connect(
    host='localhost',
    user='support_user',
    passwd=DB_USER_PASS,
    database='support_db'
)


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


def add_user(user_id: int, username: str = 'клиент', user_status: str = 'regular') -> None:
    add_query = f'''INSERT INTO user (user_id, username, user_status) VALUES
    ("{user_id}", "{username}", "{user_status}")'''

    exec_query_without_resp(query=add_query)


def add_theme(name: str) -> None:
    add_query = f'INSERT INTO theme (name) VALUES ("{name}")'

    exec_query_without_resp(query=add_query)


def add_message(user: int, theme: int, message_text: str, false_priority: int = 0) -> None:
    add_query = f'''INSERT INTO message (user, theme, message_text, false_priority) VALUES
    ("{user}", "{theme}", "{message_text}", "{str(false_priority)}")'''

    exec_query_without_resp(query=add_query)


if __name__ == '__main__':
    add_user(user_id=123456, username='ejyou', user_status='technic')
    add_theme(name='server issues')
    # add_message(user=1, theme=1, message_text="I've got a problem. Can you help me? It's emergency!!!", false_priority=3)
