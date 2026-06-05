from fastapi import FastAPI

app = FastAPI()      # Create FastAPI Backend application

@app.get("/tasks")
def get_tasks():     #Runs when the API is called.
    return [
        {
            "id": 1,
            "title": "Buy milk"
        },
        {
            "id": 2,
            "title": "Learn FastAPI"
        }
    ]