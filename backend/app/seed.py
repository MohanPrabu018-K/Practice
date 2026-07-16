"""Seed script: full production data with trailers, cast/crew."""
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.database import engine, Base, SessionLocal
from app.models import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROWS = ["A","B","C","D","E","F"]; COLS = 10

MOVIES = [
    {"title":"Inception","description":"A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.","poster_url":"https://image.tmdb.org/t/p/w500/edv5CZvWj09upOsy2Y6IwDhK8bt.jpg","genre":"Sci-Fi","duration":148,"language":"English","is_upcoming":False,"trailer_url":"https://www.youtube.com/embed/YoHD9XEInc0","cast_crew":{"director":"Christopher Nolan","cast":["Leonardo DiCaprio","Joseph Gordon-Levitt","Elliot Page","Tom Hardy"]}},
    {"title":"Interstellar","description":"A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","poster_url":"https://image.tmdb.org/t/p/w500/gEU2QniE6E77NI6lCU6MxlNBvIx.jpg","genre":"Sci-Fi","duration":169,"language":"English","is_upcoming":False,"trailer_url":"https://www.youtube.com/embed/zSWdZVtXT7E","cast_crew":{"director":"Christopher Nolan","cast":["Matthew McConaughey","Anne Hathaway","Jessica Chastain","Michael Caine"]}},
    {"title":"The Dark Knight","description":"When the menace known as the Joker wreaks havoc on Gotham, Batman must accept one of the greatest psychological tests.","poster_url":"https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911B6EMW4QxII0O.jpg","genre":"Action","duration":152,"language":"English","is_upcoming":False,"trailer_url":"https://www.youtube.com/embed/EXeTwQWrcwY","cast_crew":{"director":"Christopher Nolan","cast":["Christian Bale","Heath Ledger","Aaron Eckhart","Michael Caine"]}},
    {"title":"Parasite","description":"Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.","poster_url":"https://image.tmdb.org/t/p/w500/7IiTTgloJzvGI1TAYymCfbfl3vT.jpg","genre":"Thriller","duration":132,"language":"Korean","is_upcoming":False,"trailer_url":"https://www.youtube.com/embed/5xH0HfJHsaY","cast_crew":{"director":"Bong Joon-ho","cast":["Song Kang-ho","Lee Sun-kyun","Cho Yeo-jeong","Choi Woo-shik"]}},
    {"title":"Dune","description":"A noble family becomes embroiled in a war for control over the galaxy's most valuable asset while its heir becomes troubled by visions of a dark future.","poster_url":"https://image.tmdb.org/t/p/w500/d5NXSklXo0qyIYkgV94XAgMIckC.jpg","genre":"Sci-Fi","duration":155,"language":"English","is_upcoming":False,"trailer_url":"https://www.youtube.com/embed/n9xhJrPXop4","cast_crew":{"director":"Denis Villeneuve","cast":["Timothée Chalamet","Zendaya","Rebecca Ferguson","Oscar Isaac"]}},
    {"title":"Jananayagan","description":"A powerful political drama following the journey of a common man who rises to become the voice of the people, fighting corruption and injustice in the system.","poster_url":"https://image.tmdb.org/t/p/w500/qJ2tW6WMUDux911B6EMW4QxII0O.jpg","genre":"Drama","duration":165,"language":"Tamil","is_upcoming":False,"trailer_url":"https://www.youtube.com/embed/example","cast_crew":{"director":"R. K. Selvamani","cast":["Vijay","Keerthy Suresh","Prakash Raj","Nassar"]}},
]

THEATRES = [{"name":"PVR Cinemas","location":"Phoenix Mall, Velachery","city":"Chennai"},{"name":"INOX","location":"Forum Mall, Koramangala","city":"Bangalore"},{"name":"Cinepolis","location":"Central Mall, Jayanagar","city":"Bangalore"}]
SEAT_CATEGORIES = [{"name":"Silver","price_multiplier":1.0,"color":"#1b5e20"},{"name":"Gold","price_multiplier":1.5,"color":"#e65100"},{"name":"Platinum","price_multiplier":2.0,"color":"#6a1b9a"}]
COUPONS = [{"code":"WELCOME50","discount_percent":50,"max_uses":100,"min_order_amount":0,"expires_at":(datetime.utcnow()+timedelta(days=90)).isoformat()},{"code":"FLAT100","discount_percent":0,"max_uses":50,"min_order_amount":500,"expires_at":(datetime.utcnow()+timedelta(days=30)).isoformat()}]

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    today = datetime.now().replace(hour=0,minute=0,second=0,microsecond=0)

    demo = User(username="demo",email="demo@example.com",hashed_password=pwd_context.hash("demo123"),role="user",phone="9876543210")
    admin = User(username="admin",email="admin@moviebooker.com",hashed_password=pwd_context.hash("admin123"),role="admin",phone="9999999999")
    db.add_all([demo,admin]); db.flush()

    cats = {}
    for c in SEAT_CATEGORIES:
        sc = SeatCategory(**c); db.add(sc); db.flush(); cats[c["name"]] = sc

    for c in COUPONS:
        db.add(Coupon(code=c["code"],discount_percent=c["discount_percent"],max_uses=c["max_uses"],min_order_amount=c["min_order_amount"],expires_at=datetime.fromisoformat(c["expires_at"]),is_active=True,used_count=0))

    for tdata in THEATRES:
        t = Theatre(**tdata); db.add(t); db.flush()
        screen_count = 3 if "PVR" in t.name else (2 if "INOX" in t.name else 4)
        for s in range(1, screen_count+1): db.add(Screen(theatre_id=t.id, name=f"Screen {s}", total_rows=6, total_cols=10))

    screens = db.query(Screen).all()
    releases = [today + timedelta(days=d) for d in range(-2, 5)]
    for mi, mdata in enumerate(MOVIES):
        rd = releases[mi % len(releases)]
        mdata["release_date"] = rd
        m = Movie(**mdata); db.add(m); db.flush()
        if m.is_upcoming: continue
        for si in range(3):
            sc = screens[(mi*2+si) % len(screens)]
            show = ShowTiming(movie_id=m.id, screen_id=sc.id, show_time=rd + timedelta(days=1, hours=10+si*4), base_price=200.0+si*100)
            db.add(show); db.flush()
            for row in ROWS:
                for num in range(1, COLS+1):
                    cat_id = cats["Platinum"].id if row in ("E","F") else (cats["Gold"].id if row in ("C","D") else cats["Silver"].id)
                    db.add(Seat(show_timing_id=show.id, row_label=row, seat_number=num, category_id=cat_id))
    db.commit(); db.close()
    print(f"Seeded: {len(MOVIES)} movies, {len(THEATRES)} theatres, demo/admin users, 3 seat categories, 2 coupons")

if __name__ == "__main__": seed()
