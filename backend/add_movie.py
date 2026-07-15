"""Add Jananayagan movie."""
from datetime import datetime, timedelta
from database import SessionLocal
from models import Movie, ShowTiming, Seat

ROWS = ["A", "B", "C", "D", "E", "F"]
COLS = 10

db = SessionLocal()

movie = Movie(
    title="Jananayagan",
    description="A powerful political drama following the journey of a common man who rises to become the voice of the people, fighting corruption and injustice in the system.",
    poster_url="https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911B6EMW4QxII0O.jpg",
    genre="Drama",
    duration=165,
    language="Tamil",
)
db.add(movie)
db.flush()

today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

for idx, hour in enumerate([11, 18]):
    timing = ShowTiming(
        movie_id=movie.id,
        hall_name=f"Hall {idx + 1}",
        show_time=today + timedelta(days=idx + 1, hours=hour),
        price=250.0 + idx * 100,
    )
    db.add(timing)
    db.flush()

    for row in ROWS:
        for num in range(1, COLS + 1):
            db.add(Seat(
                show_timing_id=timing.id,
                row_label=row,
                seat_number=num,
            ))

title = movie.title
db.commit()
db.close()
print(f"Added: {title} (Tamil, Drama, 165 min)")
print(f"  - 2 show timings, 120 seats")
