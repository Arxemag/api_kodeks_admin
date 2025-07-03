import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import json


class KodeksGroupLinker:
    def __init__(self):
        self.base_url = "http://suntd.kodeks.expert:1210"
        self.username = "kodeks"
        self.password = "skedoks"
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(self.username, self.password)
        self._init_headers()

    def _init_headers(self):
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })

    def get_current_group_ids(self) -> list[str]:
        url = f"{self.base_url}/admin/dir?n=2"
        response = self.session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        input_tag = soup.find("input", {"id": "grps_1"})
        if not input_tag:
            raise ValueError("Не найден grps_1")

        value = input_tag.get("value", "")
        parsed = json.loads(value)
        return parsed.get("kw", [])

    def add_group_to_docs_catalog(self, group_id: str, com="Техэксперт"):
        group_ids = self.get_current_group_ids()
        if group_id in group_ids:
            return {"status": "ok", "message": f"Группа {group_id} уже добавлена"}

        updated_groups = group_ids + [group_id]

        data = {
            "path": "/docs/",
            "type": "3",
            "to": "kodeks6.dbs",
            "com": com,
            "trademark": "1",
            "setauth": "set",
            "auth_type": "1",
            "grps_1": json.dumps({"kw": updated_groups}),
            "grps_5": json.dumps({"kw": updated_groups}),
            "grps_3": "",
            "Support": "",
            "action": "save",
            "n": "2"
        }

        url = f"{self.base_url}/admin/dir"
        response = self.session.post(url, data=data)
        response.raise_for_status()

        return {"status": "ok", "message": f"Группа {group_id} успешно добавлена в каталог"}


if __name__ == "__main__":
    try:
        print("Запуск скрипта...")
        linker = KodeksGroupLinker()

        # Проверка авторизации
        test_response = linker.session.get(f"{linker.base_url}/admin")
        if test_response.status_code == 200:
            print("Авторизация успешна!")
        else:
            print("Ошибка авторизации")

        result = linker.add_group_to_docs_catalog("399")
        print("Результат:", result)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")