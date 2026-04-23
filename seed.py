from database import SessionLocal 
from models import Role 


session = SessionLocal()

try: 
    session.query(Role).delete()

    roles = [
        Role(name="admin"),
        Role(name="user")
    ]

    session.add_all(roles)
    session.commit()
finally:
        session.close()