import requests
import json
from typing import Dict, Any


class KodeksCabinetCreator:
    """
    Класс для создания кабинета в системе Kodeks с полным циклом аутентификации.
    """

    def __init__(self):
        """Инициализация клиента с базовыми настройками."""
        self.base_url = "http://suntd.kodeks.expert:1210"
        self.session = requests.Session()
        self.session.verify = False  # Отключаем проверку SSL для тестовых целей
        self.login = "kodeks"
        self.password = "skedoks"

        # Настройка заголовков
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json"
        })

    def authenticate(self) -> bool:
        """
        Проходит базовую аутентификацию и получает куки.

        Returns:
            bool: True если аутентификация прошла успешно
        """
        auth_url = f"{self.base_url}/infoboard/login"

        try:
            # Базовая HTTP аутентификация
            auth_response = self.session.post(
                auth_url,
                auth=(self.login, self.password),
                timeout=10
            )

            if auth_response.status_code != 200:
                print(f"❌ Ошибка аутентификации: {auth_response.status_code}")
                return False

            # Дополнительные куки
            self.session.cookies.update({
                "lastVDir": "/docs",
                "Kodeks": "1750203046"
            })

            print("✅ Аутентификация успешна")
            return True

        except Exception as e:
            print(f"❌ Ошибка при аутентификации: {str(e)}")
            return False

    def create_cabinet_from_template(self) -> Dict[str, Any]:
        """
        Создает кабинет по шаблону из JSON-файла.

        Returns:
            Словарь с результатом операции
        """
        # Сначала аутентифицируемся
        if not self.authenticate():
            return {
                "status": "error",
                "message": "Authentication failed"
            }

        # Загружаем шаблон
        try:
            with open("cabinet_template.json", "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to load template: {str(e)}"
            }

        # GraphQL запрос
        query = """
        mutation EditConfig($input: ConfigInput!) {
            editConfig(input: $input) {
                id
                title
            }
        }
        """

        # Подготовка конфига - преобразуем widgets в JSON строку
        config["id"] = ""  # Очищаем ID для создания нового кабинета
        if "widgets" in config and isinstance(config["widgets"], list):
            config["widgets"] = json.dumps(config["widgets"])

        payload = {
            "operationName": "EditConfig",
            "query": query,
            "variables": {
                "input": config
            }
        }

        try:
            response = self.session.post(
                f"{self.base_url}/infoboard/graphql?context=docs",
                json=payload,
                timeout=15
            )

            # Логирование
            print(f"HTTP Status: {response.status_code}")
            print(f"Response: {response.text[:500]}")

            result = response.json()

            if "errors" in result:
                return {
                    "status": "error",
                    "message": "GraphQL Error",
                    "details": result["errors"],
                    "response": result
                }

            if not result.get("data", {}).get("editConfig", {}).get("id"):
                return {
                    "status": "error",
                    "message": "Server didn't return cabinet ID",
                    "response": result
                }

            return {
                "status": "success",
                "data": result["data"]["editConfig"]
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "type": type(e).__name__
            }


if __name__ == "__main__":
    creator = KodeksCabinetCreator()

    print("Пытаемся создать кабинет...")
    result = creator.create_cabinet_from_template()

    if result["status"] == "success":
        cabinet = result["data"]
        print(f"✅ Успешно создан кабинет ID: {cabinet['id']}")
        print(f"Название: {cabinet.get('title', 'Не указано')}")
    else:
        print(f"❌ Ошибка: {result.get('message')}")
        if "details" in result:
            print("Детали ошибки:", json.dumps(result["details"], indent=2, ensure_ascii=False))
        if "response" in result:
            print("Полный ответ:", json.dumps(result["response"], indent=2, ensure_ascii=False))