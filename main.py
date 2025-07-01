from fastapi import FastAPI
from pydantic import BaseModel
from services.cabinet import create_cabinet
from services.group import create_group
from services.user import create_user

app = FastAPI(title="Kodeks Automation API")


class CabinetRequest(BaseModel):
    title: str


class GroupRequest(BaseModel):
    name: str
    gn: str = ""
    cmd: str = ""


class UserRequest(BaseModel):
    uid: str
    psw: str
    name: str
    org: str
    pos: str
    mail: str
    telephon: str
    grp: list[int]


@app.post("/cabinet")
def api_create_cabinet(req: CabinetRequest):
    return create_cabinet(req.title)


@app.post("/group")
def api_create_group(req: GroupRequest):
    return create_group(req.name, req.gn, req.cmd)


@app.post("/user")
def api_create_user(req: UserRequest):
    return create_user(
        uid=req.uid, psw=req.psw, name=req.name, org=req.org,
        pos=req.pos, mail=req.mail, telephon=req.telephon, grp=req.grp
    )
