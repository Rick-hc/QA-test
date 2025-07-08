from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from .db import Base

class QA(Base):
    __tablename__ = "qa"

    q_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)
    pdf_url: Mapped[str] = mapped_column(String, nullable=True)

class SearchLog(Base):
    __tablename__ = "search_log"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_query: Mapped[str] = mapped_column(Text)
    candidates: Mapped[str] = mapped_column(Text)
    selected_q2: Mapped[str | None] = mapped_column(Text, nullable=True)
    topk: Mapped[int] = mapped_column()
