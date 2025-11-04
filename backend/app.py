# ===============================================================
# 💰 Expense Tracker Backend (FastAPI + MongoDB Atlas)
# ===============================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from datetime import datetime

# ===============================================================
# 🌐 FastAPI App Setup
# ===============================================================

app = FastAPI(title="Expense Tracker API", version="1.0")

# Allow frontend apps (React, Vue, etc.) to access this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===============================================================
# ☁️ MongoDB Atlas Connection
# ===============================================================

MONGO_URI = (
    "mongodb+srv://sau70134_db_user:vp7X2srVRqS12onl@dsamagmscaiml."
    "bttnnzu.mongodb.net/?retryWrites=true&w=majority&appName=DSAMAGMSCAIML"
)

# Connect to MongoDB Atlas Cluster
client = MongoClient(MONGO_URI)

# Database and Collection
db = client["expense_tracker"]
collection = db["expenses"]

# ===============================================================
# 🧾 Data Model
# ===============================================================

class Expense(BaseModel):
    name: str
    category: str
    amount: float
    date: str = datetime.now().strftime("%Y-%m-%d")

# ===============================================================
# 🧩 API Routes
# ===============================================================

@app.get("/")
def home():
    """Root endpoint to check connection."""
    return {"message": "💰 Expense Tracker API connected to MongoDB Atlas Cloud!"}


@app.post("/add_expense")
def add_expense(expense: Expense):
    """Add a new expense record to MongoDB."""
    collection.insert_one(expense.dict())
    return {"message": "✅ Expense added successfully to MongoDB Cloud!"}


@app.get("/expenses")
def get_expenses():
    """Fetch all expenses sorted by date (latest first)."""
    data = list(collection.find({}, {"_id": 0}))
    data.sort(key=lambda x: x["date"], reverse=True)
    return data


@app.get("/summary")
def get_summary():
    """Get category-wise expense totals."""
    pipeline = [
        {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}},
        {"$project": {"_id": 0, "category": "$_id", "total": 1}},
    ]
    summary = list(collection.aggregate(pipeline))
    return summary


@app.delete("/delete_expense/{name}")
def delete_expense(name: str):
    """Delete an expense by name."""
    result = collection.delete_one({"name": name})
    if result.deleted_count > 0:
        return {"message": f"🗑️ Expense '{name}' deleted successfully."}
    return {"message": f"⚠️ Expense '{name}' not found."}


@app.put("/update_expense/{name}")
def update_expense(name: str, updated_expense: Expense):
    """Update an expense record by name."""
    result = collection.update_one(
        {"name": name}, {"$set": updated_expense.dict()}
    )
    if result.matched_count > 0:
        return {"message": f"✏️ Expense '{name}' updated successfully."}
    return {"message": f"⚠️ Expense '{name}' not found."}

# ===============================================================
# ✅ End of File
# ===============================================================
