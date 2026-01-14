# app/api/routes/wage.py
from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.db_async import get_db
from app.service.ser_wage import WageService

wageRou = APIRouter()


@wageRou.post("/upload")
async def upload_reports(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    content = await file.read()
    await WageService.upload_csv(db, content)
    return {"status": "ok"}

@wageRou.post("/add")
async def create_wage(
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    return await WageService.create(db, payload)


@wageRou.get("/")
async def list_reports(
    db: AsyncSession = Depends(get_db),
):
    return await WageService.list_wages(db)


@wageRou.get("/pagination")
async def list_wages(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
):
    return await WageService.list_paginated(
        db=db,
        page=page,
        page_size=page_size,
    )
    
    
# FastAPI PATCH endpoint (required)
@wageRou.patch("/{report_id}")
async def update_report(
    report_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
):
    return await WageService.update_partial(db, report_id, payload)




@wageRou.get("/list_filtered_reports")
async def list_filtered_reports(
    page: int = 1,
    page_size: int = 10,
    sort_by: str | None = None,
    sort_order: str | None = "asc",
    source: str | None = None,
    deal_stage: str | None = None,
    lead_owner: str | None = None,
    first_name: str | None = None,
    last_name: str | None = None,
    company: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    return await WageService.list_filtered_reports(
        db,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        sort_order=sort_order,
        source=source,
        deal_stage=deal_stage,
        lead_owner=lead_owner,
        first_name=first_name,
        last_name=last_name,
        company=company,
    )
