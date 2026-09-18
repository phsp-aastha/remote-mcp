from fastmcp import FastMCP
import os
import sqlite3

OS_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
mcp = FastMCP(name="ExpenseTracker")

def init_db():
    with sqlite3.connect(OS_PATH) as c:
        c.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                description TEXT DEFAULT '' 
            )
            """
        )
init_db()

@mcp.tool
def add_expense(date: str, amount: float, category: str, subcategory: str = "", description: str = "") -> dict:
    """Add a new expense to the database."""
    with sqlite3.connect(OS_PATH) as c:
        curr= c.execute(
            "INSERT INTO expenses (date, description, amount, category, subcategory) VALUES (?, ?, ?, ?, ?)",
            (date, description, amount, category, subcategory),
        )
        return {"status": "success", "id": curr.lastrowid}

@mcp.tool
def get_expenses() -> list[dict]:
    """Retrieve all expenses from the database."""
    with sqlite3.connect(OS_PATH) as c:
        curr= c.execute("SELECT * FROM expenses ORDER BY id ASC")
        cols= [d[0] for column in curr.description]
        return [dict(zip(cols,r)) for r in curr.fetchall()]

if __name__ == "__main__":
    mcp.run()   