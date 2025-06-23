from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette.status import HTTP_204_NO_CONTENT

from expense_tracker_backend.core.Oauth import get_current_user
from expense_tracker_backend.schemas.user import ExpenseCreate,ExpenseUpdate, ExpenseRead
from expense_tracker_backend.services.expense import ExpenseService
from expense_tracker_backend.core.database import get_session
from expense_tracker_backend.models.user import User

router = APIRouter(prefix="/expenses", tags=["Expense"])

@router.post("/create", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
async def create_expense(
        expense : ExpenseCreate,
        db: AsyncSession = Depends(get_session),
        current_user : User = Depends(get_current_user)
):
    service = ExpenseService(db, current_user.id)
    return await service.expense_create(expense)

@router.get("/", response_model=List[ExpenseRead])
async def read_expense(
        db: AsyncSession = Depends(get_session),
        current_user : User = Depends(get_current_user)
):
    service = ExpenseService(db, current_user.id)
    return await service.expense_read()

@router.get("/{expense_id}", response_model=ExpenseRead)
async def read_one_expense(
        expense_id : int,
        db : AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    service = ExpenseService(db, current_user.id)
    expense = await service.get_expense(expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="expense not found")
    return expense

@router.put("/update/{expense_id}", response_model=ExpenseRead)
async def update_expense(
        expense_id : int,
        expense_data : ExpenseUpdate,
        db: AsyncSession = Depends(get_session),
        current_user: User =Depends(get_current_user)
):
    service = ExpenseService(db, current_user.id)
    expense_result = await service.expense_update(expense_id, expense_data)
    if not expense_result:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense_result

@router.delete("/{expense_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_expense(
        expense_id: int,
        current_user : User = Depends(get_current_user),
        db : AsyncSession = Depends(get_session),
):
    service = ExpenseService(db, current_user.id)
    success = await service.expense_delete(expense_id)
    if not success:
        raise HTTPException(status_code=404, detail = "Expense not found to delete")
    return None
