# app/haystack/iv/iv_sql_component.py
import logging
from sqlalchemy import select, or_, func
from haystack import component
from haystack.dataclasses import Document
from app.db.db_sync import SessionLocal
from app.db.models.m_innov import Innov

logger = logging.getLogger(__name__)

@component
class ORMComponent:
    """
    EXACT lookup on innov table.
    Use for precise filters: account_id, company, first_name, last_name, lead_owner, deal_stage.
    """

    @component.output_types(documents=list[Document], count=int)
    def run(self, query: str, limit: int = 50, count_only: bool = False):
        db = SessionLocal()
        try:
            filters = or_(
                Innov.lead_owner.ilike(f"%{query}%"),
                Innov.source.ilike(f"%{query}%"),
                Innov.deal_stage.ilike(f"%{query}%"),
                Innov.account_id == query,
                Innov.first_name.ilike(f"%{query}%"),
                Innov.last_name.ilike(f"%{query}%"),
                Innov.company.ilike(f"%{query}%"),
            )
            
            if count_only:
                stmt = select(func.count()).select_from(Innov).where(filters)
                count = db.execute(stmt).scalar_one()
                return {"count": count}
            
            stmt = (
                select(Innov)
                .where(filters)
                .order_by(Innov.mdate.desc())
                .limit(limit)
            )

            logger.info("--------------- Executing SQL search with query: %s", query)

            rows = db.execute(stmt).scalars().all()

            documents = [
                Document(
                    id=str(r.id),
                    content=r.content or "",
                    meta={
                        "company": r.company,
                        "account_id": r.account_id,
                        "deal_stage": r.deal_stage,
                        "lead_owner": r.lead_owner,
                        "mdate": r.mdate.isoformat(),
                        "source": "sql",
                    },
                )
                for r in rows
            ]

            return {"documents": documents}
        finally:
            db.close()
