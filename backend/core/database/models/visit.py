from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base


class VisitORM(Base):
    __tablename__ = "visits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    counter: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    repr_cols_num: int = 2
