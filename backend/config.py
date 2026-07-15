import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:1823@localhost:5432/movie_booking"
)

SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 60 * 24  # 24 hours

CORS_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
