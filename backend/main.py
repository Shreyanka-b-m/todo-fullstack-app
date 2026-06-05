from fastapi import FastAPI
from sqlalchemy import text
from database import engine
from schemas import TaskCreate
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


@app.post("/tasks")
def create_task(task: TaskCreate):

    with engine.connect() as connection:

        connection.execute(
            text(
                "INSERT INTO tasks (title) VALUES (:title)"
            ),
            {
                "title": task.title
            }
        )

        connection.commit()

    return {
        "message": "Task created successfully"
    }



# Let's Understand Connection code clearly
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







# Let's Understand Post Request Slowly
# FastAPI Route
# @app.post("/tasks")

# Means:

# When somebody sends POST request
# to /tasks
# run this function
# Input
# task: TaskCreate

# Means:

# Accept JSON

# {
#     "title": "something"
# }

# and convert it into Python object.

# SQL Query
# INSERT INTO tasks (title)
# VALUES (:title)

# This is the same SQL you manually ran earlier.

# Remember:

# INSERT INTO tasks (title)
# VALUES ('Buy milk');

# Same thing.

# Dynamic Value
# "title": task.title

# Suppose user sends:

# {
#     "title": "Learn React"
# }

# FastAPI replaces:

# :title

# with:

# Learn React
# Commit
# connection.commit()

# Very important.

# Without this:

# Insert happens
# ↓
# Database not saved

# Think:

# Save Button

# for database changes.