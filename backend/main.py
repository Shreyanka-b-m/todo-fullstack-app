from fastapi import FastAPI
from sqlalchemy import text
from database import engine

app = FastAPI()   # Create FastAPI Backend application

@app.get("/tasks")      # Runs when the API is called.
def get_tasks():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT * FROM tasks")
        )

        tasks = []

        for row in result:
            tasks.append(
                {
                    "id": row.id,
                    "title": row.title,
                    "completed": bool(row.completed)
                }
            )

        return tasks




# Let's Understand This
# Open connection
# with engine.connect() as connection:

# means:

# FastAPI
#     ↓
# Connect to MariaDB
# Execute SQL
# text("SELECT * FROM tasks")

# means:

# SELECT * FROM tasks;

# which you already ran manually.

# Loop through results

# Suppose MariaDB returns:

# id	title	completed
# 1	Buy milk	1
# 2	Learn FastAPI	0

# This loop:

# for row in result:

# reads each row.

# Return JSON

# Eventually:

# return tasks

# returns:

# [
#   {
#     "id": 1,
#     "title": "Buy milk",
#     "completed": true
#   },
#   {
#     "id": 2,
#     "title": "Learn FastAPI",
#     "completed": false
#   }
# ]