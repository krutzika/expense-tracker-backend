from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from expense_tracker_backend.core.Oauth import get_current_user
from expense_tracker_backend.core.database import get_session
from expense_tracker_backend.models.user import User
from expense_tracker_backend.schemas.user import ExpenseStatsResponse, ExpenseComparisonResponse
from expense_tracker_backend.services.statistics import ExpenseStatistics

router = APIRouter(prefix="/statistics", tags=["Summary"])

@router.get("/", response_model=ExpenseStatsResponse)
async def expense_statistics(
        days : int = Query(30, ge=1, le=365, description="Time range in days"),
        db : AsyncSession = Depends(get_session),
        current_user : User = Depends(get_current_user)
):
    try:
        get_statistics = ExpenseStatistics(user_id=current_user.id, db=db)
        return await get_statistics.get_expense_breakdown(days=days)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while fetching statistics"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No summary found"
        )

@router.get("/trend", response_model=ExpenseComparisonResponse )
async def expense_comparison(
        days : int,
        db : AsyncSession = Depends(get_session),
        current_user : User = Depends(get_current_user)
):
    try:
        get_expense_comparison = ExpenseStatistics(user_id=current_user.id, db=db, days=days)
        return await get_expense_comparison.get_comparison(days=days)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error while fetching statistics"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No summary found"
        )