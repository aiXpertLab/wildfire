from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from pgvector.sqlalchemy import Vector

from app.db.models import Base, BaseMixin

class Innov(Base, BaseMixin):
    __tablename__ = "innov"
    
    __table_args__ = (
        Index("idx_reports_lead_owner", "lead_owner"),
        Index("idx_reports_source", "source"),
        Index("idx_reports_deal_stage", "deal_stage"),
        Index("idx_reports_account_id", "account_id"),
        Index("idx_reports_first_name", "first_name"),
        Index("idx_reports_last_name", "last_name"),
        Index("idx_reports_company", "company"),
        Index("idx_reports_mdate", "mdate"),
    )

    lead_owner: Mapped[str] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(String(255), nullable=True)
    deal_stage: Mapped[str] = mapped_column(String(100), nullable=True)
    account_id: Mapped[str] = mapped_column(String(32), nullable=True)

    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    company: Mapped[str] = mapped_column(String(255), nullable=True)
    memo: Mapped[dict] = mapped_column(JSONB, nullable=True)  # store arbitrary JSON


    content: Mapped[str] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=True)
