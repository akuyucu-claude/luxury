from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Brand
from app.schemas import BrandCreate, BrandRead

router = APIRouter(tags=["brands"])


@router.get("/brands", response_model=list[BrandRead])
async def list_brands(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).order_by(Brand.name))
    brands = result.scalars().all()
    return brands


@router.get("/brands/{brand_id}", response_model=BrandRead)
async def get_brand(brand_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Brand).where(Brand.id == brand_id))
    brand = result.scalar_one_or_none()
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand


@router.post("/brands", response_model=BrandRead, status_code=201)
async def create_brand(brand_data: BrandCreate, db: AsyncSession = Depends(get_db)):
    # Check for duplicate name
    result = await db.execute(select(Brand).where(Brand.name == brand_data.name))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Brand with this name already exists")

    brand = Brand(**brand_data.model_dump())
    db.add(brand)
    await db.commit()
    await db.refresh(brand)
    return brand
