Для получения всех групп, мы можем обратиться на страницу /users/groups

Для создания новой группы мы должны отправить запрос /users/groups/name=test&gn=&cmd=
Где name = Имя группы
    gn = Аббревиатура
    cmd = Команда



Для создания пользователя мы должны обратиться к /users/users и передать туда параметры для создания пользователя.

uid	testpo
psw	12345
name	Тест Тестович Тестовый
org	Выдуманное
pos	Аналогичная
mail	chtototam@may.ru
telephon	+9992124345
end
grp	4
grp	48
grp	49
grp	321
grp	362
set

Выглядит это так = /users/user/uid=testpo&psw=12345&name=Тест Тестович Тестовый9&org=Выдуманное&pos=Аналогичная&mail=chtototam@may.ru&telephon=+9992124345&end=&grp=4&grp=48&grp=49&grp=321&grp=362&set=

Вопрос, где взять номера групп, очень просто = читаем в creating a group.txt



docker build -t kodeks-admin-api .
docker run -p 8000:8000 kodeks-admin-api


http://localhost:8000/docs
