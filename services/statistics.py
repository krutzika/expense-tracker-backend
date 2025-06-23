from datetime import timedelta, datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, func

from expense_tracker_backend.models.expense import Expense


async def get_expense_statistics(user_id : int, days: int, db : AsyncSession):
    start_date = datetime.utcnow() - timedelta(days=days)
    query = select(
        Expense.category,
        func.sum(Expense.amount)
    ).where(
        Expense.user_id==user_id,
        Expense.created_at>= start_date
    ).group_by(Expense.category)
    summary = await db.execute(query)
    return {row[0]: row[1] for row in summary.all()}
