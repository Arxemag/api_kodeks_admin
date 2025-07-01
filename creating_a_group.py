import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://suntd.kodeks.expert:1210"
USERNAME = "kodeks"
PASSWORD = "skedoks"

auth = HTTPBasicAuth(USERNAME, PASSWORD)


def get_all_groups():
    url = f"{BASE_URL}/users/groups"
    response = requests.get(url, auth=auth)

    if response.ok:
        print("Группы получены успешно.")
        return response.text
    else:
        print(f"Ошибка получения групп: {response.status_code}")
        return None


def create_group(name: str, gn: str = "", cmd: str = ""):
    params = {
        "name": name,
        "gn": gn,
        "cmd": cmd
    }
    url = f"{BASE_URL}/users/groups"
    response = requests.get(url, params=params, auth=auth)

    if response.ok:
        print(f"Группа '{name}' создана успешно.")
        return response.text
    else:
        print(f"Ошибка создания группы: {response.status_code}")
        return None

if __name__ == "__main__":
    print("Все группы:")
    print(get_all_groups())

