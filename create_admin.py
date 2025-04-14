from app import create_app
from app.models.user import User
from app import db

app = create_app()

with app.app_context():
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@admin.com",
            is_admin=True
        )
        admin.set_password("iamadmin")
        db.session.add(admin)
        db.session.commit()
        print("Admin créé avec succès !")
    else:
        print("Un admin existe déjà")