import requests

def create_user(uid, psw, name, org, pos, mail, telephon, grp: list):
    auth = ("kodeks", "skedoks")

    # Формируем query-параметры
    params = {
        "uid": uid,
        "psw": psw,
        "name": name,
        "org": org,
        "pos": pos,
        "mail": mail,
        "telephon": telephon,
        "end": ""
    }

    # Добавляем группы
    for group_id in grp:
        params.setdefault("grp", []).append(group_id)

    # Завершаем командой
    params["set"] = ""

    resp = requests.get(
        "http://suntd.kodeks.expert:1210/users/user",
        params=params,
        auth=auth
    )
    return {"url": resp.url, "status": resp.status_code}
