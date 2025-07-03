import requests  # Для выполнения HTTP-запросов
from requests.auth import HTTPBasicAuth  # Для базовой HTTP-аутентификации
from bs4 import BeautifulSoup  # Для парсинга HTML-страниц
import json  # Для работы с JSON-данными


# Основной класс для работы с админкой Kodeks
class KodeksAdmin:
    def __init__(self):
        """Инициализация класса - настройка базовых параметров подключения"""
        # Базовый URL адрес админки
        self.base_url = "http://suntd.kodeks.expert:1210"
        # Данные для базовой аутентификации (логин и пароль)
        self.auth = HTTPBasicAuth("kodeks", "skedoks")

        # Создаем сессию для сохранения состояния (куки, заголовки и т.д.)
        self.session = requests.Session()
        # Устанавливаем аутентификацию для сессии
        self.session.auth = self.auth
        # Обновляем заголовки запросов
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0",  # Притворяемся браузером
            "Content-Type": "application/x-www-form-urlencoded"  # Тип отправляемых данных
        })

    def log(self, message):
        """Метод для логирования сообщений с префиксом [LOG]"""
        print(f"[LOG] {message}")

    def get_all_groups(self):
        """Получение списка всех групп пользователей из системы"""
        # Формируем URL для запроса списка групп
        url = f"{self.base_url}/users/groups"
        # Отправляем GET-запрос через сессию
        resp = self.session.get(url)

        # Парсим HTML-ответ с помощью BeautifulSoup
        soup = BeautifulSoup(resp.text, "html.parser")
        # Создаем словарь для хранения результатов (название группы -> ID группы)
        result = {}

        # Ищем все ссылки в HTML
        for link in soup.find_all("a", href=True):
            href = link["href"]  # Получаем значение атрибута href
            # Проверяем, что это ссылка на группу
            if "grp?grp=" in href:
                # Извлекаем ID группы из URL (все что после "grp=")
                group_id = href.split("=")[-1]
                # Получаем название группы (текст ссылки) и убираем лишние пробелы
                group_name = link.text.strip()
                # Добавляем в словарь
                result[group_name] = group_id
        return result

    def group_exists(self, name):
        """Проверка существования группы по имени"""
        # Просто проверяем, есть ли имя группы в списке всех групп
        return name in self.get_all_groups()

    def get_group_id_by_name(self, name):
        """Получение ID группы по её имени"""
        # Получаем все группы
        groups = self.get_all_groups()
        # Возвращаем ID группы или None, если группы нет
        return groups.get(name)

    def create_group(self, name):
        """Создание новой группы пользователей"""
        self.log(f"Создание группы: {name}")
        # Базовый URL для работы с группами
        url = f"{self.base_url}/users/groups"
        # Отправляем GET-запрос с параметром имени группы
        response = self.session.get(f"{self.base_url}/users/groups?name={name}")

        # Проверяем успешность запроса
        if response.status_code == 200:
            self.log(f"Группа '{name}' создана.")
            # Возвращаем ID созданной группы
            return self.get_group_id_by_name(name)
        else:
            # В случае ошибки выбрасываем исключение с деталями
            raise Exception(f"Ошибка при создании группы: {response.status_code} {response.text}")

    def get_current_catalog_group_ids(self):
        """Получение списка ID групп, подключенных к каталогу /docs"""
        # URL страницы настроек каталога
        url = f"{self.base_url}/admin/dir?n=2"
        response = self.session.get(url)
        # Парсим HTML
        soup = BeautifulSoup(response.text, "html.parser")
        # Ищем input-элемент с ID "grps_1"
        input_tag = soup.find("input", {"id": "grps_1"})

        # Проверяем, что элемент найден
        if not input_tag:
            raise ValueError("grps_1 не найден")
        # Получаем значение атрибута value
        value = input_tag.get("value", "")
        # Парсим JSON и извлекаем список ID групп
        return json.loads(value).get("kw", [])

    def add_group_to_catalog(self, group_id):
        """Добавление группы к каталогу /docs"""
        # Получаем текущий список ID групп в каталоге
        current_ids = self.get_current_catalog_group_ids()
        # Проверяем, не добавлена ли группа уже
        if group_id in current_ids:
            self.log(f"Группа {group_id} уже подключена к каталогу.")
            return

        # Формируем обновленный список ID групп
        updated_ids = current_ids + [group_id]
        # Данные для отправки на сервер
        data = {
            "path": "/docs/",  # Путь к каталогу
            "type": "3",  # Тип каталога
            "to": "kodeks6.dbs",  # База данных
            "com": "Техэксперт",  # Комментарий
            "trademark": "1",  # Торговая марка
            "setauth": "set",  # Флаг установки прав
            "auth_type": "1",  # Тип авторизации
            "grps_1": json.dumps({"kw": updated_ids}),  # Новые группы в формате JSON
            "grps_5": json.dumps({"kw": updated_ids}),  # Новые группы в формате JSON
            "grps_3": "",  # Пустое поле
            "Support": "",  # Поддержка
            "action": "save",  # Действие - сохранение
            "n": "2"  # Номер операции
        }

        # URL для отправки данных
        url = f"{self.base_url}/admin/dir"
        # Отправляем POST-запрос с данными
        response = self.session.post(url, data=data)

        # Проверяем результат
        if response.status_code == 200:
            self.log(f"Группа {group_id} успешно добавлена к каталогу /docs.")
        else:
            self.log(f"❌ Не удалось добавить группу в каталог. Статус: {response.status_code}")
            self.log(f"Ответ сервера: {response.text}")

    def user_exists(self, login):
        """Проверка существования пользователя по логину"""
        # URL страницы со списком пользователей
        url = f"{self.base_url}/users/users"
        response = self.session.get(url)
        # Парсим HTML и проверяем наличие логина в тексте страницы
        soup = BeautifulSoup(response.text, "html.parser")
        return login in soup.text

    def create_user(self, login, password, group_id):
        """Создание нового пользователя и добавление его в группу"""
        self.log(f"Создание пользователя: {login}")

        # Основные параметры пользователя
        params = {
            "uid": login,  # Логин
            "psw": password,  # Пароль
            "name": login,  # Имя (совпадает с логином)
            "org": "",  # Организация (пусто)
            "pos": "",  # Должность (пусто)
            "mail": "",  # Email (пусто)
            "telephon": "",  # Телефон (пусто)
            "end": "",  # Дата окончания доступа (пусто)
            "set": ""  # Флаг (пусто)
        }

        # Параметры группы (может быть несколько групп)
        grp_params = [("grp", str(group_id))]  # Преобразуем ID группы в строку

        # URL для создания пользователя
        url = f"{self.base_url}/users/users"
        # Отправляем GET-запрос с объединенными параметрами
        response = self.session.get(url, params=[*params.items(), *grp_params])

        # Проверяем результат
        if response.status_code == 200:
            self.log(f"Пользователь {login} создан и добавлен в группу {group_id}.")
        else:
            self.log(f"❌ Не удалось создать пользователя. Статус: {response.status_code}")
            self.log(f"Ответ сервера: {response.text}")


def full_flow(org_name: str, login: str, password: str):
    """Полный процесс: создание группы, добавление в каталог и создание пользователя"""
    # Создаем экземпляр класса KodeksAdmin
    admin = KodeksAdmin()

    # 1. Работа с группой
    if admin.group_exists(org_name):
        # Если группа существует - получаем её ID
        group_id = admin.get_group_id_by_name(org_name)
        admin.log(f"Группа уже существует. ID: {group_id}")
    else:
        # Если группы нет - создаем её
        group_id = admin.create_group(org_name)

    # 2. Добавляем группу в каталог /docs
    admin.add_group_to_catalog(group_id)

    # 3. Работа с пользователем
    if admin.user_exists(login):
        # Если пользователь существует - просто логируем
        admin.log(f"Пользователь {login} уже существует.")
    else:
        # Если пользователя нет - создаем его
        admin.create_user(login, password, group_id)

    admin.log("✅ Вся процедура выполнена.")
