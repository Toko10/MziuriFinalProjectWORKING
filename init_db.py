from ext import app, db
from models import User, Artist

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = User(username="admin")
    admin.set_password("adminpass")
    admin.create()

    artist1 = Artist(
        name="2slimey",
        debut_year=2023,
        image="2slimey.jpg"
    )
    artist2 = Artist(
        name="xaviersobased",
        debut_year=2021,
        image="xaviersobased.jpg"
    )
    artist3 = Artist(
        name="slayr",
        debut_year=2022,
        image="slayr.png"
    )
    artist4 = Artist(
        name="che",
        debut_year=2021,
        image="che.jpg"
    )
    artist5 = Artist(
        name="prettifun",
        debut_year=2023,
        image="prettifun.jpg"
    )

    artist1.create()
    artist2.create()
    artist3.create()
    artist4.create()
    artist5.create()