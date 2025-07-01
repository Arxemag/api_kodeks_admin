import requests
import json


class KodeksCabinetCreator:
    """
    Класс для создания кабинета в системе Kodeks через GraphQL API.
    Позволяет создавать кабинеты с заданными параметрами.
    Для понимания какие параметры мы можем передовать нужно перейти на
    http://suntd.kodeks.expert:1210/infoboard/graphql?context=docs
    Там есть вся документация.
    """

    def __init__(self):
        """Инициализация клиента с базовыми настройками."""
        self.base_url = "http://suntd.kodeks.expert:1210"
        self.session = requests.Session()
        self.session.verify = False  # Отключаем проверку SSL для тестовых целей

        # Настройка кук для аутентификации
        self.session.cookies.update({
            "Auth": "a29kZWtzOnNrZWRva3M=",
            "Kodeks": "1750203046",
            "KodeksData": "XzI0OTY4NzI2MzNfMTc5MzIwNQ==",
            "lastVDir": "/docs"
        })

        # Установка заголовков запроса
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        })

    def create_cabinet(self, title="Тестовый кабинет"):
        """
        Создает новый кабинет с указанным названием.

        Args:
            title (str): Название создаваемого кабинета

        Returns:
            dict: Результат операции (успех/ошибка) и данные созданного кабинета
        """
        # GraphQL запрос для создания/редактирования конфигурации кабинета
        query = """
        mutation EditConfig($input: ConfigInput!) {
            editConfig(input: $input) {
                id
                title
            }
        }
        """

        # Параметры для создания кабинета
        variables = {
            "input": {
                "id": "",  # Пустой ID означает создание нового кабинета
                "title": title,
                "widgets": "[{\"documents\":[816800077]}]",  # ID документов для виджета
                "palette": {
                    "primary": {
                        "main": "#E36E26",
                        "dark": "#d85a00",
                        "text": "#ffffff",
                        "link": "#ffffff"
                    },
                    "secondary": {
                        "main": "#f8f8f8",
                        "dark": "#d8d8d8",
                        "text": "#333333",
                        "link": "#dd7217"
                    }
                }
            }
        }

        try:
            # Отправка запроса к GraphQL API
            response = self.session.post(
                f"{self.base_url}/infoboard/graphql?context=docs",
                json={"query": query, "variables": variables},
                timeout=10
            )

            result = response.json()

            # Обработка ошибок GraphQL
            if "errors" in result:
                return {
                    "status": "error",
                    "message": "GraphQL Error",
                    "details": result["errors"]
                }

            # Возвращаем данные созданного кабинета
            return result.get("data", {}).get("editConfig", {})

        except Exception as e:
            # Обработка исключений при выполнении запроса
            return {
                "status": "error",
                "message": str(e)
            }


if __name__ == "__main__":
    # Пример использования класса
    creator = KodeksCabinetCreator()

    print("Пытаемся создать кабинет...")
    result = creator.create_cabinet("Мой кабинет СМК")

    # Обработка и вывод результатов
    if isinstance(result, dict):
        if result.get("status") == "error":
            print(f"❌ Ошибка: {result.get('message')}")
            if "details" in result:
                print("Детали:", json.dumps(result["details"], indent=2))
        elif result.get("id"):
            print(f"✅ Успешно создан кабинет ID: {result['id']}")
            print(f"Название: {result.get('title')}")
        else:
            print("❌ Не удалось создать кабинет. Ответ сервера:")
            print(json.dumps(result, indent=2))
    else:
        print("❌ Некорректный ответ сервера")