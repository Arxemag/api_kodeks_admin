from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.kodeks_admin import KodeksAdmin

app = FastAPI()
admin = KodeksAdmin()

class CreateUserRequest(BaseModel):
    organization: str
    login: str
    password: str

@app.post("/create-user")
def create_user(request: CreateUserRequest):
    try:
        org = request.organization
        login = request.login
        psw = request.password

        if admin.group_exists(org):
            group_id = admin.get_group_id_by_name(org)
        else:
            group_id = admin.create_group(org)

        admin.add_group_to_catalog(group_id)

        if not admin.user_exists(login):
            admin.create_user(login, psw, group_id)
            return {"status": "created", "user": login}
        else:
            return {"status": "exists", "user": login}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
