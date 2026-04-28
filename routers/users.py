from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from models import User, Role
from schemas import UserIn, UserUpdate
from typing import Annotated

router = APIRouter()

@router.get("/users")
async def list_user(x_user_id: Annotated[int, Header()], db: Session = Depends(get_db)):
    user_auth = db.query(User).filter(User.id == x_user_id).first()
    if not user_auth:
        raise HTTPException(status_code=404, detail="Ususario não encontrado")
    if user_auth.role_id == 1:
        users = db.query(User).all()
        return users
    else:
        return user

@router.post("/users")
async def create_user(x_user_id: Annotated[int, Header()], user_data: UserIn, db: Session = Depends(get_db)):
    user_auth = db.query(User).filter(User.id == x_user_id).first()
    if not user_auth:
        raise HTTPException(status_code=404, detail="Usuario não encontrado") 
    if user_auth.role_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        role = db.query(Role).filter(Role.id == user_data.role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role não encontrada")

    mail_auth = db.query(User).filter(User.email == user_data.email).first()
    if mail_auth:
        raise HTTPException(status_code=409, detail="Esse email ja esta sendo usado")
    else:
        new_user = User(
            name = user_data.name,
            email = user_data.email,
            role_id = user_data.role_id
        )


        try: 
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except Exception:
            db.rollback()
            raise HTTPException(status_code=400, detail="Erro ao criar usuario")
        

@router.get("/users/{id}")
async def list_user_byId(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    return user


@router.delete("/users/{id}")
async def delete_user(x_user_id: Annotated[int, Header()], id: int, db: Session = Depends(get_db)):
    user_auth = db.query(User).filter(User.id == x_user_id).first()
    if not user_auth:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    if user_auth.role_id != 1:
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario não encontrado")
        db.delete(user)
        db.commit()
        return {'Mensagem: Usuario deletado com sucesso'}


@router.put("/users/{id}")
async def update_user(id: int, user_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario não encontrado")
    if user_data.name is not None:
        user.name = user_data.name
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.role_id is not None:
        user.role_id = user_data.role_id

    db.commit()
    db.refresh(user)
    return user
