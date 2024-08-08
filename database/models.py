from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    repr_cols_num = 2
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class CounterORM(Base):
    __tablename__ = "counter"

    id: Mapped[int] = mapped_column(primary_key=True)
    counter: Mapped[int] = mapped_column(default=0)

    repr_cols_num = 2


class BlogsORM(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    image_uri: Mapped[Optional[str]]
    created_at: Mapped[str]

    repr_cols_num = 3


# class MessagesORM(Base):
#     __tablename__ = "messages"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     message: Mapped[str]
#     user_ip: Mapped[str]
#     saved_at: Mapped[str]

#     repr_cols_num = 2
