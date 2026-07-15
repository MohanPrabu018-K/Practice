# Movie Ticket Booking App — Implementation Plan

## 1. Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Frontend    | React 18 (Vite), React Router v6  |
| Styling     | Plain CSS / CSS Modules           |
| Backend     | Python FastAPI                    |
| ORM         | SQLAlchemy                        |
| Database    | PostgreSQL                        |
| DB Driver   | psycopg2-binary                   |
| HTTP Client | Axios (frontend → backend)        |

---

## 2. Architecture Overview

```mermaid
flowchart TD
    subgraph Frontend[React Frontend - Vite]
        A[MovieListPage] --> B[MovieDetailPage]
        B --> C[SeatSelectionPage]
        C --> D[BookingConfirmationPage]
        D --> E[BookingSuccessPage]
    end

    subgraph Backend[FastAPI Backend]
        F[Movies Router]
        G[ShowTimings Router]
        H[Bookings Router]
    end

    subgraph Database[PostgreSQL Database]
        I[(movies)]
        J[(show_timings)]
        K[(seats)]
        L[(bookings)]
        M[(booking_seats)]
    end

    Frontend -->|REST API calls| Backend
    Backend -->|SQLAlchemy + psycopg2| Database
```

---

## 3. Data Model

### `movies`

| Column       | Type         | Constraints           |
|-------------|-------------|-----------------------|
| id          | SERIAL       | PK                    |
| title       | VARCHAR(255) | NOT NULL              |
| description | TEXT         |                       |
| poster_url  | VARCHAR(500) |                       |
| genre       | VARCHAR(100) |                       |
| duration    | INTEGER      | (minutes)             |
| language    | VARCHAR(100) |                       |

### `show_timings`

| Column    | Type         | Constraints              |
|-----------|-------------|---------------------------|
| id        | SERIAL       | PK                        |
| movie_id  | INTEGER      | FK → movies.id, NOT NULL  |
| hall_name | VARCHAR(100) | NOT NULL                  |
| show_time | TIMESTAMP    | NOT NULL                  |
| price     | NUMERIC(8,2) | NOT NULL                  |

### `seats`

| Column         | Type         | Constraints                  |
|----------------|-------------|-------------------------------|
| id             | SERIAL       | PK                            |
| show_timing_id | INTEGER      | FK → show_timings.id, NOT NULL |
| row_label      | VARCHAR(5)   | NOT NULL (A, B, C...)         |
| seat_number    | INTEGER      | NOT NULL (1, 2, 3...)         |
| is_booked      | BOOLEAN      | DEFAULT FALSE                 |

### `bookings`

| Column            | Type          | Constraints              |
|-------------------|---------------|---------------------------|
| id                | SERIAL        | PK                        |
| user_name         | VARCHAR(255)  | NOT NULL                  |
| user_email        | VARCHAR(255)  | NOT NULL                  |
| booking_reference | VARCHAR(20)   | UNIQUE, NOT NULL          |
| total_amount      | NUMERIC(8,2)  | NOT NULL                  |
| booking_time      | TIMESTAMP     | NOT NULL (default now())  |

### `booking_seats`

| Column    | Type    | Constraints                  |
|-----------|---------|------------------------------|
| id        | SERIAL  | PK                           |
| booking_id| INTEGER | FK → bookings.id, NOT NULL   |
| seat_id   | INTEGER | FK → seats.id, NOT NULL      |
| UNIQUE    | —       | (booking_id, seat_id)        |

---

## 4. API Endpoints

| Method | Path                           | Description                      |
|--------|--------------------------------|----------------------------------|
| GET    | `/api/movies`                  | List all movies (optional `?genre=` & `?language=` filters) |
| GET    | `/api/movies/{movie_id}`       | Single movie + its show timings  |
| GET    | `/api/show-timings/{id}/seats` | Seat layout for a specific show  |
| POST   | `/api/bookings`               | Create a booking                 |
| GET    | `/api/bookings/{reference}`    | Retrieve booking by reference    |

**`POST /api/bookings` request body:**

```json
{
  "user_name": "Mohan",
  "user_email": "mohan@example.com",
  "show_timing_id": 3,
  "seat_ids": [12, 13, 14]
}
```

**Response:**

```json
{
  "booking_reference": "MOV-ABC123",
  "total_amount": 750.00,
  "seats": ["A-4", "A-5", "A-6"],
  "movie_title": "Inception",
  "show_time": "2026-07-20T18:30:00",
  "hall_name": "Hall 1"
}
```

---

## 5. Frontend Route & Component Tree

```
App
├── Header (logo, nav)
├── Routes
│   ├── / → MovieListPage
│   │       ├── SearchBar
│   │       ├── FilterTabs (genre, language)
│   │       └── MovieCard[] (poster, title, genre, duration)
│   ├── /movie/:id → MovieDetailPage
│   │       ├── MovieInfo (poster, description, genre, lang, duration)
│   │       └── ShowTimingCard[] (hall, time, price → "Book" button)
│   ├── /book/:showTimingId → SeatSelectionPage
│   │       ├── ScreenIndicator
│   │       ├── SeatMap (grid: rows A–F × cols 1–10)
│   │       │   └── Seat[] (color-coded: available / selected / booked)
│   │       ├── SeatLegend
│   │       └── BookingSummary (seats, price, total → user form)
│   └── /booking/:reference → BookingSuccessPage
│           └── BookingDetails (reference, movie, time, seats, amount)
└── Footer
```

---

## 6. Seat Map Design

- **Rows**: A through F (6 rows)
- **Columns**: 1 through 10 (10 seats per row)
- **Total**: 60 seats per hall per show
- **Colors**:
  - 🟢 Green = Available
  - 🔵 Blue = Selected
  - 🔴 Red = Booked

---

## 7. Project Structure (Simplified — Flat)

```
Agentic AI/
├── backend/
│   ├── main.py                  # FastAPI app + ALL routes combined
│   ├── database.py              # SQLAlchemy engine (PostgreSQL), session
│   ├── config.py                # DB connection URL + app settings
│   ├── models.py                # All 5 ORM models in one file
│   ├── schemas.py               # All Pydantic schemas in one file
│   ├── seed.py                  # Seed script: tables + data
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx             # React entry point
│       ├── App.jsx              # Router + layout wrapper
│       ├── App.css              # ALL styles in one file
│       ├── api.js               # Axios + all API calls
│       ├── MovieListPage.jsx    # Page: movie grid + filters
│       ├── MovieDetailPage.jsx  # Page: movie info + show timings
│       ├── SeatSelectionPage.jsx# Page: seat map + booking form
│       ├── BookingSuccessPage.jsx# Page: booking confirmation
│       ├── Header.jsx           # Top nav bar
│       ├── MovieCard.jsx        # Single movie card
│       ├── Seat.jsx             # Single seat square
│       ├── SeatMap.jsx          # 6×10 seat grid
│       └── ShowTimingCard.jsx   # Single show timing row
```

---

## 8. PostgreSQL Configuration

**Connection string**: `postgresql://username:password@localhost:5432/movie_booking`

Set via environment variable `DATABASE_URL` — the `config.py` reads from `os.getenv()` with a sensible local default.

### Steps to set up PostgreSQL locally:

1. Ensure PostgreSQL is installed and running
2. Create the database:
   ```sql
   CREATE DATABASE movie_booking;
   ```
3. Tables are auto-created on app startup by `Base.metadata.create_all()` in `database.py`
4. Run `seed.py` once to populate movies, show timings, and seats

---

## 9. Data Flow — Booking Journey

```mermaid
sequenceDiagram
    participant U as User
    participant F as React Frontend
    participant B as FastAPI Backend
    participant D as PostgreSQL

    U->>F: Browse movies on home page
    F->>B: GET /api/movies
    B->>D: SELECT * FROM movies
    D-->>B: movies list
    B-->>F: JSON response
    F-->>U: Render movie cards

    U->>F: Click a movie
    F->>B: GET /api/movies/{id}
    B->>D: SELECT movie + show_timings JOIN
    D-->>B: movie + timings
    B-->>F: JSON response
    F-->>U: Render detail + show cards

    U->>F: Click Book on a show timing
    F->>B: GET /api/show-timings/{id}/seats
    B->>D: SELECT seats WHERE show_timing_id = X
    D-->>B: seats list with is_booked flags
    B-->>F: JSON response
    F-->>U: Render interactive seat map

    U->>F: Select seats + fill name/email + click Confirm
    F->>B: POST /api/bookings
    B->>D: BEGIN<br/>SELECT seats FOR UPDATE<br/>Check all seats NOT booked<br/>UPDATE seats SET is_booked=TRUE<br/>INSERT INTO bookings<br/>INSERT INTO booking_seats<br/>COMMIT
    D-->>B: success
    B-->>F: booking_reference + details
    F-->>U: Redirect to success page

    U->>F: View booking success
    F->>B: GET /api/bookings/{reference}
    B->>D: SELECT booking + seats JOIN
    D-->>B: booking details
    B-->>F: JSON response
    F-->>U: Show ticket summary
```

---

## 10. Key Design Decisions

1. **No authentication** — user provides name + email at booking time. A booking reference code is generated server-side (`MOV-` + 6 random alphanumeric chars).

2. **Pessimistic locking for seat booking** — the `POST /api/bookings` wraps the operation in a transaction using `SELECT ... FOR UPDATE` on the target seat rows. This prevents double-booking under concurrent requests. If any seat is already booked, the transaction rolls back and returns `409 Conflict`.

3. **Seat pre-generation** — 60 seats per show timing are created by the seed script, so no dynamic seat generation at runtime.

4. **CORS enabled** — FastAPI configured to allow the Vite dev server origin (`http://localhost:5173`).

5. **Database** — PostgreSQL for production-grade concurrency handling, `SERIAL` for auto-increment IDs, `BOOLEAN` for the `is_booked` flag, and `NUMERIC(8,2)` for price/amount fields.

---

## 11. Seed Data (sample)

- **5 movies**: Inception, Interstellar, The Dark Knight, Parasite, Dune
- **2 show timings per movie** (morning + evening)
- **60 seats per show timing** (A1–F10)
- Total: ~600 seat rows pre-generated
