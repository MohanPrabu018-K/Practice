"""Pagination helper for list endpoints."""
from sqlalchemy import select, func
from sqlalchemy.orm import Session


class Paginator:
    """Generic paginator for SQLAlchemy queries."""

    def __init__(self, db: Session, base_query, page: int = 1, limit: int = 12):
        self.db = db
        self.base_query = base_query
        self.page = max(1, page)
        self.limit = min(max(1, limit), 100)  # cap at 100

    def paginate(self) -> dict:
        """Execute paginated query and return data with metadata."""
        total = self.db.scalar(
            select(func.count()).select_from(self.base_query.subquery())
        )

        total_pages = max(1, (total + self.limit - 1) // self.limit)
        offset = (self.page - 1) * self.limit

        items = self.db.execute(
            self.base_query.offset(offset).limit(self.limit)
        ).scalars().all()

        return {
            "items": items,
            "total": total,
            "page": self.page,
            "limit": self.limit,
            "total_pages": total_pages,
        }
