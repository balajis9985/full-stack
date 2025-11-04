# app.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from pymongo import MongoClient
import os

app = FastAPI()

# ✅ Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with your frontend domain: "https://fro-ekvq.onrender.com"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "your_mongo_connection_uri_here")
client = MongoClient(MONGO_URI)
db = client["expense_tracker"]
collection = db["expenses"]

# ✅ Data model
class Expense(BaseModel):
    name: str
    category: str
    amount: float
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))

# ✅ Add Expense
@app.post("/add_expense")
def add_expense(expense: Expense):
    expense_dict = expense.dict()
    collection.insert_one(expense_dict)
    return {"message": "✅ Expense added successfully"}

# ✅ Get all expenses
@app.get("/expenses")
def get_expenses():
    expenses = list(collection.find({}, {"_id": 0}))
    return expenses

# ✅ Summary of expenses by category
@app.get("/summary")
def get_summary():
    pipeline = [
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}
    ]
    result = list(collection.aggregate(pipeline))
    return [{"category": r["_id"], "total": r["total"]} for r in result]

@app.get("/")
def root():
    return {"message": "✅ Smart Expense Tracker Backend Running"}
