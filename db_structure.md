## ПОЛЬЗОВАТЕЛИ [user]
#### 1) id пользователя
#### 2) username пользователя
#### 3) статус пользователя (т.е. овощ или овощ техподдержки)
+---+----------+--------------+----------------+ <br> 
| id | user_id | username | user_status | <br>
+---+----------+--------------+----------------+ <br>
#### SQL:
CREATE TABLE user( <br>
id INT NOT NULL AUTO_INCREMENT, <br>
user_id INT NOT NULL UNIQUE, <br>
username VARCHAR(30) NULL DEFAULT "клиент", <br>
user_status ENUM('regular', 'technic') NOT NULL, <br>
PRIMARY KEY (id));


## ФИКСИРОВАННЫЕ ТЕМЫ [theme]
#### 1) name
+---+--------+ <br>
| id | name | <br>
+---+--------+
#### SQL:
CREATE TABLE theme( <br>
id INT NOT NULL AUTO_INCREMENT, <br>
name VARCHAR(30) NOT NULL UNIQUE, <br>
PRIMARY KEY (id));


## СООБЩЕНИЯ [message]
#### 1) id пользователя (из таблицы user)
#### 2) тема (из таблицы theme)
#### 3) мнимый приоритет
#### 4) истинный приоритет (т.е. дата написания сообщения) 
#### 5) текст сообщения
+---+------+---------+------------------+----------------+--------------------+ <br> 
| id | user | theme | false_priority | true_priority | message_text | <br>
+---+------+---------+------------------+----------------+--------------------+ 
#### SQL:
CREATE TABLE message( <br>
id INT NOT NULL AUTO_INCREMENT, <br>
user INT NOT NULL, <br>
theme INT NOT NULL, <br>
false_priority ENUM('0', '1', '2') NOT NULL DEFAULT '0', <br>
true_priority TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, <br>
message_text TEXT NOT NULL, <br>
PRIMARY KEY (id), <br>
FOREIGN KEY (user) REFERENCES user(id), <br>
FOREIGN KEY (theme) REFERENCES theme(id));







<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>
class Character(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDERS = [
        (MALE, 'Man'),
        (FEMALE, 'Woman')
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=1, choices=GENDERS, default=MALE)
