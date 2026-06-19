from app import create_app, bcrypt
from app.models import db
from app.models.user import User

app = create_app()

with app.app_context():

    hashed_password = bcrypt.generate_password_hash("$Password123!").decode('utf-8')

    admin = User(
        username="admin",
        email="admin@mail.com",
        password=hashed_password,
        role="admin"
    )

    db.session.add(admin)
    db.session.commit()

    print("Admin créé avec succès")
