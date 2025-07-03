import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlencode


class KodeksPermissionManager:

    def __init__(self):
        self.base_url = "http://suntd.kodeks.expert:1210"
        self.auth = HTTPBasicAuth("kodeks", "skedoks")
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Requested-With": "XMLHttpRequest"
        }

    def set_permissions(self) -> dict:
        params = {
            "setup2": "",
            "n": "2",
            "set": "",
            "acl_unstoragero": "",
            "acl_unstorage": "",
            "acl_unstoragefull": "",
            "acl_unprint": "",
            "unprinttext": "Установлен административный запрет на выполнение операции печати.",
            "acl_unsave": "",
            "unsavetext": "Установлен административный запрет на выполнение операции сохранения в файл.",
            "acl_uncopy": "",
            "uncopytext": "Установлен административный запрет на выполнение операции копирования.",
            "uncopylength": "0",
            "acl_infoboard_k001": "",
            "acl_infoboard_p000a": '{"kw":["1"]}',
            "acl_infoboard_p000b": "",
            "acl_infoboard_p000f": "",
            "infoboard_p000g": "on",
            "acl_infoboard_p000g": '{"kw":["1","399"]}',
            "infoboard_p000h": "on",
            "acl_infoboard_p000h": '{"kw":["1","399","491"]}',
            "acl_inspectactuallinks": "",
            "desiredtab": "-1",
            "desiredtabas": "-1"
        }

        try:
            url = f"{self.base_url}/admin/dirs"
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                auth=self.auth,
                timeout=20
            )

            print("\n=== ДЕТАЛИ ЗАПРОСА ===")
            print(f"Фактический URL запроса: {response.request.url}")
            print(f"Метод: {response.request.method}")
            print(f"Заголовки: {response.request.headers}")

            print("\n=== ОТВЕТ СЕРВЕРА ===")
            print(f"Статус: {response.status_code}")
            print(f"Ответ ({len(response.text)} символов):")
            print(response.text[:500] + ("..." if len(response.text) > 500 else ""))

            if response.status_code == 200:
                return {"status": "success", "message": "Права успешно назначены"}
            return {"status": "error", "message": f"HTTP {response.status_code}", "response": response.text}

        except Exception as e:
            return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    print("=== ТЕСТ НАЗНАЧЕНИЯ ПРАВ ===")
    manager = KodeksPermissionManager()

    print("\nЗапуск процесса назначения прав...")
    result = manager.set_permissions()

    print("\n=== РЕЗУЛЬТАТ ===")
    if result["status"] == "success":
        print("✅ Права успешно назначены!")
    else:
        print(f"❌ Ошибка: {result.get('message')}")
        if "response" in result:
            print("Ответ сервера:", result["response"][:500])