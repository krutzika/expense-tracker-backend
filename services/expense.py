from itsdangerous.serializer import is_text_serializer
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from sqlmodel import select

from expense_tracker_backend.models.expense import Expense
from expense_tracker_backend.schemas.user import ExpenseCreate, ExpenseRead, ExpenseUpdate

class ExpenseService :
    def __init__(self, db : AsyncSession, user_id : int):
        self.db = db
        self.user_id = user_id

    async def expense_create(self, expense: ExpenseCreate) -> Expense :
        db_expense = Expense(**expense.dict(exclude_unset=True), user_id=self.user_id)
        self.db.add(db_expense)
        await self.db.commit()
        await self.db.refresh(db_expense)
        return db_expense

    async def get_expense(self, expense_id : int) -> Optional[Expense]:
        expense = await self.db.get(Expense, expense_id)
        if expense and expense.user_id == self.user_id:
            return expense
        return None

    async def expense_update (
            self,
            expense_id : int,
            expense_update : ExpenseUpdate
    ) -> Optional[Expense] :
        expense = await self.get_expense(expense_id)
        if not expense:
            return None
        expense_data = expense_update.dict(exclude_unset=True)
        for key, value in expense_data.items():
            setattr(expense, key, value)
        self.db.add(expense)
        await self.db.commit()
        await self.db.refresh(expense)
        return expense

    async def expense_read(self ) -> List[ExpenseRead]:
        expense = await self.db.exec(
            select(Expense).where(Expense.user_id==self.user_id).order_by(Expense.created_at.desc())
        )
        return expense.all()

    async def expense_delete(
            self,
            expense_id : int
    ) -> bool :
        expense = await self.get_expense(expense_id)
        if not expense:
            return False
        await self.db.delete(expense)
        await self.db.commit()
        return True
