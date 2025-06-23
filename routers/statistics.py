from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from expense_tracker_backend.core.Oauth import get_current_user
from expense_tracker_backend.core.database import get_session
from expense_tracker_backend.models.user import User
from expense_tracker_backend.schemas.user import ExpenseStatsResponse
from expense_tracker_backend.services.statistics import get_expense_statistics

router = APIRouter(prefix="/statistics", tags=["Summary"])

@router.get("/", response_model=ExpenseStatsResponse)
async def expense_statistics(
        days : int = Query(30, ge=1, le=365, description="Time range in days"),
        db : AsyncSession = Depends(get_session),
        current_user : User = Depends(get_current_user)
):
    try:
        return get_expense_statistics(current_user.id, days, db)
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