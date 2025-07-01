import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://suntd.kodeks.expert:1210"
USERNAME = "kodeks"
PASSWORD = "skedoks"

auth = HTTPBasicAuth(USERNAME, PASSWORD)

def create_user(
    uid: str,
    psw: str,
    name: str,
    org: str,
    pos: str,
    mail: str,
    telephon: str,
    groups: list[int]
):
    """
    Создаёт пользователя с указанными параметрами и привязывает к группам.
    """
    base_url = f"{BASE_URL}/users/users"

    # Базовые параметры
    params = {
        "uid": uid,
        "psw": psw,
        "name": name,
        "org": org,
        "pos": pos,
        "mail": mail,
        "telephon": telephon,
        "end": "",
        "set": ""
    }

    # Список групп как несколько одинаковых ключей grp=...
    grp_params = [("grp", str(g)) for g in groups]

    # Собираем всё вместе
    response = requests.get(base_url, params=[*params.items(), *grp_params], auth=auth)

    if response.ok:
        print(f"Пользователь '{uid}' успешно создан.")
        return response.text
    else:
        print(f"Ошибка создания пользователя: {response.status_code}")
        return response.text


if __name__ == "__main__":
    create_user(
        uid="testpo",
        psw="12345",
        name="Тест Тестович Тестовый",
        org="Выдуманное",
        pos="Аналогичная",
        mail="chtototam@may.ru",
        telephon="+9992124345",
        groups=[1, 474, 362, 8, 5]
    )
