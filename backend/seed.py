"""Seed script: creates tables and populates sample data."""

from datetime import datetime, timedelta
from passlib.context import CryptContext
from database import engine, Base, SessionLocal
from models import User, Movie, ShowTiming, Seat

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ROWS = ["A", "B", "C", "D", "E", "F"]
COLS = 10  # seats 1..10

MOVIES = [
    {
        "title": "Inception",
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "poster_url": "https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg",
        "genre": "Sci-Fi",
        "duration": 148,
        "language": "English",
    },
    {
        "title": "Interstellar",
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "poster_url": "https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg",
        "genre": "Sci-Fi",
        "duration": 169,
        "language": "English",
    },
    {
        "title": "The Dark Knight",
        "description": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological tests.",
        "poster_url": "https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911B6EMW4QxII0O.jpg",
        "genre": "Action",
        "duration": 152,
        "language": "English",
    },
    {
        "title": "Parasite",
        "description": "A poor family, the Kims, con their way into becoming the servants of a rich family, the Parks. But their easy life gets complicated.",
        "poster_url": "https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg",
        "genre": "Thriller",
        "duration": 132,
        "language": "Korean",
    },
    {
        "title": "Dune",
        "description": "A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.",
        "poster_url": "https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg",
        "genre": "Sci-Fi",
        "duration": 155,
        "language": "English",
    },
]


def seed():
    # Drop all tables and recreate (clean slate)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Demo user
    demo_user = User(
        username="demo",
        email="demo@example.com",
        hashed_password=pwd_context.hash("demo123"),
    )
    db.add(demo_user)
    db.flush()
    print("  - Demo user: demo / demo123")

    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    for movie_data in MOVIES:
        movie = Movie(**movie_data)
        db.add(movie)
        db.flush()  # get movie.id

        # 2 show timings per movie
        for idx, hour in enumerate([11, 18]):
            timing = ShowTiming(
                movie_id=movie.id,
                hall_name=f"Hall {idx + 1}",
                show_time=today + timedelta(days=idx + 1, hours=hour),
                price=250.0 + idx * 100,  # 250 / 350
            )
            db.add(timing)
            db.flush()  # get timing.id

            # 60 seats per show
            for row in ROWS:
                for num in range(1, COLS + 1):
                    db.add(Seat(
                        show_timing_id=timing.id,
                        row_label=row,
                        seat_number=num,
                    ))

    db.commit()
    db.close()
    print("Database seeded successfully!")
    print(f"  - {len(MOVIES)} movies")
    print(f"  - {len(MOVIES) * 2} show timings")
    print(f"  - {len(MOVIES) * 2 * len(ROWS) * COLS} seats")


if __name__ == "__main__":
    seed()
