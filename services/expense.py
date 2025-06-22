from itsdangerous.serializer import is_text_serializer
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from sqlmodel import select

from expense_tracker_backend.models.expense import Expense
from expense_tracker_backend.schemas.user import ExpenseCreate, ExpenseRead, ExpenseUpdate

async def expense_create(
        expense: ExpenseCreate,
        user_id : int,
        db : AsyncSession
) -> Expense :
    db_expense = Expense(**expense.dict(), user_id=user_id)
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

async def get_expense(
        expense_id : int,
        user_id: int,
        db : AsyncSession
) -> Optional[Expense]:
    expense = await db.get(Expense, expense_id)
    if expense and expense.user_id == user_id:
        return expense
    return None

async def expense_update (
        expense_id : int,
        expense_update : ExpenseUpdate,
        user_id : int,
        db : AsyncSession
) -> Optional[Expense] :
    expense = await get_expense(expense_id, user_id, db)
    if not expense:
        return None
    expense_data = expense_update.dict(exclude_unset=True)
    for key, value in expense_data.items():
        setattr(expense, key, value)
    db.add(expense)
    await db.commit()
    await db.refresh(expense)
    return expense

async def expense_read(
        user_id : int,
        db: AsyncSession
) -> List[ExpenseRead]:
    expense = await db.exec(
        select(Expense).where(Expense.user_id==user_id).order_by(Expense.created_at.desc())
    )
    return expense.all()

async def expense_delete(
        expense_id : int,
        user_id : int,
        db: AsyncSession
) -> bool :
    expense = await get_expense(expense_id, user_id, db)
    if not expense:
        return False
    db.delete(expense)
    await db.commit()
    return True
