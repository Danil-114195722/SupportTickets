## ПОЛЬЗОВАТЕЛИ [user]
#### 1) id пользователя
#### 2) статус пользователя (т.е. овощ или овощ техподдержки)
+---+----------+--------------+----------------+ <br> 
| id | user_id | username | user_status | <br>
+---+----------+--------------+----------------+ 


## ФИКСИРОВАННЫЕ ТЕМЫ [theme] (возможно)
#### 1) name
+---+--------+ <br> 
| id | name | <br>
+---+--------+

## СООБЩЕНИЯ
#### 1) id пользователя 
#### 2) тема
#### 3) мнимый приоритет
#### 4) истинный приоритет (т.е. дата написания сообщения) 
#### 5) текст сообщения
+---+------+---------+------------------+----------------+--------------------+ <br> 
| id | user | theme | false_priority | true_priority | message_text | <br>
+---+------+---------+------------------+----------------+--------------------+ 








<br><br><br><br><br><br><br><br><br><br><br><br><br><br>
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
