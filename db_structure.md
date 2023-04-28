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


[//]: # (## ФИКСИРОВАННЫЕ ТЕМЫ [theme])
[//]: # (#### 1&#41; name)
[//]: # (+---+--------+ <br>)
[//]: # (| id | name | <br>)
[//]: # (+---+--------+)
[//]: # (#### SQL:)
[//]: # (CREATE TABLE theme&#40; <br>)
[//]: # (id INT NOT NULL AUTO_INCREMENT, <br>)
[//]: # (name VARCHAR&#40;30&#41; NOT NULL UNIQUE, <br>)
[//]: # (PRIMARY KEY &#40;id&#41;&#41;;)


## СООБЩЕНИЯ [ticket]
#### 1) id пользователя (из таблицы user)
#### 2) тема до 100 символов
#### 3) мнимый приоритет (0, 1 или 2)
#### 4) истинный приоритет (т.е. дата написания сообщения) 
#### 5) текст сообщения
#### 6) выполнен ли тикет (True или False)
+---+------+---------+------------------+----------------+--------------------+ <br> 
| id | user | theme | false_priority | true_priority | message_text | <br>
+---+------+---------+------------------+----------------+--------------------+ 
#### SQL:
CREATE TABLE ticket( <br>
id INT NOT NULL AUTO_INCREMENT, <br>
user INT NOT NULL, <br>
theme VARCHAR(100) NOT NULL, <br>
false_priority ENUM('0', '1', '2') NOT NULL DEFAULT '0', <br>
true_priority TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, <br>
message_text TEXT NOT NULL, <br>
done BOOLEAN NOT NULL DEFAULT 0, <br>
PRIMARY KEY (id), <br>
CONSTRAINT user_forkey FOREIGN KEY (user) REFERENCES user(id));
