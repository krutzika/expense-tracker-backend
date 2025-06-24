from datetime import timedelta, datetime
from typing import Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from expense_tracker_backend.models.expense import Expense, Category
from expense_tracker_backend.schemas.user import ExpenseStatsResponse


class ExpenseStatistics:

    def __init__(self, user_id: int, db: AsyncSession, days : int):
        self.user_id = user_id
        self.db = db
        self.days = days

    async def _get_expense_statistics(self) -> Dict[Category, float]:
        start_date = datetime.utcnow() - timedelta(days=self.days)
        query = select(
            Expense.category,
            func.sum(Expense.amount)
        ).where(
            Expense.user_id==self.user_id,
            Expense.created_at>= start_date
        ).group_by(Expense.category)
        summary = await self.db.execute(query)
        return {row[0]:row[1] for row in summary.all()}

    async def get_expense_breakdown(self) -> Dict:
        summary = await self._get_expense_statistics()
        total_spent = sum(summary.values()) if summary else 0.0

        breakdown = {}
        for category in Category:
            amount = float(summary.get(category, 0.0))
            percentage = (amount/total_spent*100) if total_spent>0 else 0.0
            breakdown[category.value] = {
                "total" : amount,
                "percentage" : percentage
            }

        return {"total spent" : total_spent, "category_breakdown": breakdown}

    async def _get_start_end_period(self, comparison_period: int) :


    async def _get_total_category_expense_periodically(self, start_date: datetime, end_date : datetime) -> Dict:

    async def get_comparison(self, days: int) -> Dict:
        start_date = datetime.utcnow() - timedelta(days=days)
        end_date = datetime.utcnow()



