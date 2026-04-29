from database import SessionLocal 
from models import Role, User


session = SessionLocal()

try: 
    session.query(Role).delete()

    roles = [
        Role(name="admin"),
        Role(name="user")
    ]

    users = [
          User(name="Pedro", email="pedro@email.com", role_id=1),
          User(name="Matheus", email="matheus@email.com", role_id=2)
    ]

    session.add_all(roles)
    session.commit()
    session.add_all(users)
    session.commit()
finally:
        session.close()