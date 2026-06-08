from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

from auth import verify_password, hash_password, create_token, get_current_user
from sqlalchemy import text
from database import engine
from schemas import TaskCreate
from sqlalchemy import text
from database import engine

app = FastAPI()   # Create FastAPI Backend application

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

@app.get("/tasks")
def get_tasks(credentials: HTTPAuthorizationCredentials = Depends(security)):

    token = credentials.credentials
    user_id = get_current_user(token)

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM tasks WHERE user_id = :user_id"),
            {"user_id": user_id}
        )

        tasks = []
        for row in result:
            tasks.append({
                "id": row.id,
                "title": row.title,
                "completed": bool(row.completed)
            })

    return tasks


@app.post("/tasks")
def create_task(
    task: TaskCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    user_id = get_current_user(token)

    with engine.connect() as connection:
        connection.execute(
            text("INSERT INTO tasks (title, user_id) VALUES (:title, :user_id)"),
            {
                "title": task.title,
                "user_id": user_id
            }
        )
        connection.commit()

    return {"message": "Task created"}


@app.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    user_id = get_current_user(token)

    with engine.connect() as connection:
        connection.execute(
            text("UPDATE tasks SET completed = TRUE WHERE id = :id AND user_id = :user_id"),
            {"id": task_id, "user_id": user_id}
        )
        connection.commit()

    return {"message": "Updated"}


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials
    user_id = get_current_user(token)

    with engine.connect() as connection:
        connection.execute(
            text("DELETE FROM tasks WHERE id = :id AND user_id = :user_id"),
            {"id": task_id, "user_id": user_id}
        )
        connection.commit()

    return {"message": "Deleted"}


@app.post("/signup")
def signup(email: str, password: str):

    hashed = hash_password(password)

    try:
        with engine.connect() as connection:
            connection.execute(
                text(
                    "INSERT INTO users (email, password) VALUES (:email, :password)"
                ),
                {
                    "email": email,
                    "password": hashed
                }
            )
            connection.commit()

    except Exception as e:
        print("SIGNUP ERROR:", e)  # keep for server logs
        raise HTTPException(
            status_code=400,
            detail="User already exists or signup failed"
        )

    return {"message": "User created successfully"}

@app.post("/login")
def login(email: str, password: str):

    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {"email": email}
        ).fetchone()

    if not result:
        return {"error": "User not found"}

    if not verify_password(password, result.password):
        return {"error": "Wrong password"}

    token = create_token({"user_id": result.id})

    return {"token": token}

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




# Understand Put Request Clearly
# 1. Path Parameter
# @app.put("/tasks/{task_id}")

# means:

# User will send:
# PUT /tasks/1
# PUT /tasks/2
# 2. Input
# task_id: int

# FastAPI automatically takes:

# /tasks/1 → task_id = 1
# 3. SQL Query
# UPDATE tasks
# SET completed = TRUE
# WHERE id = :id

# Same SQL you ran manually earlier.

# 4. Dynamic Value
# "id": task_id

# If:

# PUT /tasks/1

# Then:

# WHERE id = 1
# 5. Commit
# connection.commit()

# Again → save changes to DB




# Understand Delete Request
# 1. Route
# @app.delete("/tasks/{task_id}")

# Means:

# DELETE request to /tasks/1
# 2. SQL
# DELETE FROM tasks WHERE id = :id

# Same SQL you used manually.

# 3. Dynamic Value
# "id": task_id

# So:

# /tasks/2 → id = 2