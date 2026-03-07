from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from datetime import datetime

from app.database import get_db
from app.models import FinancialData, Brand
from app.schemas import FinancialDataRead
from app.services.financial_service import fetch_financial_for_all_brands

router = APIRouter(tags=["financial"])


@router.get("/financial/{brand_id}", response_model=list[FinancialDataRead])
async def get_financial_data(
    brand_id: int,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
):
    # Verify brand exists
    brand_result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = brand_result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    query = (
        select(FinancialData)
        .where(FinancialData.brand_id == brand_id)
        .order_by(desc(FinancialData.date))
    )

    if start_date:
        try:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.where(FinancialData.date >= start_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD")

    if end_date:
        try:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            query = query.where(FinancialData.date <= end_dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD")

    result = await db.execute(query)
    data = result.scalars().all()
    return data


@router.get("/financial/{brand_id}/latest", response_model=Optional[FinancialDataRead])
async def get_latest_financial(brand_id: int, db: AsyncSession = Depends(get_db)):
    brand_result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = brand_result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")

    query = (
        select(FinancialData)
        .where(FinancialData.brand_id == brand_id)
        .order_by(desc(FinancialData.date))
        .limit(1)
    )
    result = await db.execute(query)
    data = result.scalar_one_or_none()
    return data


@router.post("/financial/fetch")
async def trigger_financial_fetch(db: AsyncSession = Depends(get_db)):
    count = await fetch_financial_for_all_brands(db)
    return {"message": f"Fetched financial data for {count} brands"}
