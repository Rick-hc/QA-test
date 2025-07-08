import uuid
from sqlalchemy import Column, String, Text, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .db import Base

class QA(Base):
    __tablename__ = "qa"

    q_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    pdf_url = Column(String, nullable=True)

class SearchLog(Base):
    __tablename__ = "search_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_query = Column(Text, nullable=False)
    q1_list = Column(Text, nullable=False)
    selected_q2 = Column(Text, nullable=True)
    topk = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
