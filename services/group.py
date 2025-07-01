import requests

def create_group(name: str, gn: str = "", cmd: str = ""):
    auth = ("kodeks", "skedoks")
    params = {
        "name": name,
        "gn": gn,
        "cmd": cmd
    }
    resp = requests.get(
        "http://suntd.kodeks.expert:1210/users/groups",
        params=params,
        auth=auth
    )
    return {"url": resp.url, "status": resp.status_code}
