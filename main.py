from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class User(BaseModel):
    id:Optional[int] = None
    name:str
    email:str

class UserCreate(BaseModel):
    name:str
    email:str

users=[
    User(id=1,name = "John Doe", email="john@email.com"),
    User(id=2, name="Jane Smith",email="jane@email.com")
]

@app.get("/api/users",response_model=List[User])
def get_users():
    return users

@app.get("/api/user/{user_id}",response_model=User)
def get_user(user_id:int):
    user = next((u for u in users if u.id==user_id),None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/api/user",response_model=User,status_code=201)
def create_user(user: UserCreate):
    new_user = User(
        id=users[len(users)-1].id+1,
        name=user.name,
        email=user.email
    )
    users.append(new_user)
    return new_user

@app.put("/api/user",response_model=User)
def edit_user(user:User):
    existingUser = next((u for u in users if u.id==user.id),None)
    if existingUser is None:
        raise HTTPException(status_code=404, detail="User Not found")
    else:
        existingUser.name = user.name
        existingUser.email = user.email
        return existingUser
    
@app.delete("/api/user/delete/{user_id}",status_code=204)
def delete_user(user_id:int):
    global users
    users = [u for u in users if u.id!=user_id]
    