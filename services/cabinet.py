import requests

def create_cabinet(title: str):
    session = requests.Session()
    session.verify = False
    session.cookies.update({
        "Auth": "a29kZWtzOnNrZWRva3M=",
        "Kodeks": "1750203046",
        "KodeksData": "XzI0OTY4NzI2MzNfMTc5MzIwNQ==",
        "lastVDir": "/docs"
    })
    session.headers.update({
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    })

    query = """
    mutation EditConfig($input: ConfigInput!) {
        editConfig(input: $input) {
            id
            title
        }
    }
    """

    variables = {
        "input": {
            "id": "",
            "title": title,
            "widgets": "[{\"documents\":[816800077]}]",
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

    resp = session.post(
        "http://suntd.kodeks.expert:1210/infoboard/graphql?context=docs",
        json={"query": query, "variables": variables},
        timeout=10
    )
    return resp.json()
