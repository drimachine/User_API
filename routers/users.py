from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Role
from schemas import UserIn, UserUpdate

router = APIRouter()

@router.get("/users")
async def list_user(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/users")
async def create_user(user_data: UserIn, db: Session = Depends(get_db)):
    
    role = db.query(Role).filter(Role.id == user_data.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role não encontrada")

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
async def delete_user(id: int, db: Session = Depends(get_db)):
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
