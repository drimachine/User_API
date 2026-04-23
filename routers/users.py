from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User, Role
from schemas import UserIn

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