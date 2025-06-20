from fastapi import FastAPI
from expense_tracker_backend.core.database import create_db_and_tables
from expense_tracker_backend.routers import auth

app = FastAPI(title="Expense Tracker API")

@app.on_event("startup")
async def on_startup():
    await  create_db_and_tables()

app.include_router(auth.router)