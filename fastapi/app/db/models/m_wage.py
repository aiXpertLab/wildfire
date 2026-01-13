from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (String,    Integer,    Float, Date,    Text,    Index,)
from sqlalchemy.dialects.postgresql import JSONB

from pgvector.sqlalchemy import Vector

from app.db.models.m_base import Base, BaseMixin


class CanadaWage(Base, BaseMixin):
    __tablename__ = "canada_wages"

    __table_args__ = (
        Index("idx_wages_noc_code", "noc_code"),
        Index("idx_wages_province", "province"),
        Index("idx_wages_er_code", "er_code"),
        Index("idx_wages_reference_period", "reference_period"),
        Index("idx_wages_noc_prov", "noc_code", "province"),
    )

    # ---- Occupation ----
    noc_code: Mapped[str] = mapped_column(String(10), nullable=False)
    noc_title_en: Mapped[str] = mapped_column(String(255), nullable=False)
    noc_title_fr: Mapped[str] = mapped_column(String(255), nullable=False)

    # ---- Geography ----
    province: Mapped[str] = mapped_column(String(10), nullable=False)
    er_code: Mapped[str] = mapped_column(String(20), nullable=True)
    er_name_en: Mapped[str] = mapped_column(String(255), nullable=True)
    er_name_fr: Mapped[str] = mapped_column(String(255), nullable=True)

    # ---- Wages (CAD) ----
    low_wage: Mapped[int] = mapped_column(Integer, nullable=True)
    median_wage: Mapped[int] = mapped_column(Integer, nullable=True)
    high_wage: Mapped[int] = mapped_column(Integer, nullable=True)
    average_wage: Mapped[int] = mapped_column(Integer, nullable=True)
    quartile1_wage: Mapped[int] = mapped_column(Integer, nullable=True)
    quartile3_wage: Mapped[int] = mapped_column(Integer, nullable=True)

    annual_wage_flag: Mapped[bool] = mapped_column(nullable=False, default=False)

    # ---- Metadata ----
    source_2025: Mapped[str] = mapped_column(String(255), nullable=True)
    data_source_en: Mapped[str] = mapped_column(String(255), nullable=True)
    data_source_fr: Mapped[str] = mapped_column(String(255), nullable=True)

    reference_period: Mapped[str] = mapped_column(String(20), nullable=True)
    revision_date: Mapped[Date] = mapped_column(Date, nullable=True)

    # ---- Notes / Comments ----
    wage_comment_en: Mapped[str] = mapped_column(Text, nullable=True)
    wage_comment_fr: Mapped[str] = mapped_column(Text, nullable=True)

    # ---- Benefits ----
    non_wage_benefit_pct: Mapped[float] = mapped_column(Float, nullable=True)

    # ---- Optional: raw row + embedding (for search / RAG) ----
    content_en: Mapped[str] = mapped_column(Text, nullable=True)
    content_fr: Mapped[str] = mapped_column(Text, nullable=True)
