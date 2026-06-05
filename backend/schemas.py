from pydantic import BaseModel  
  
# Pydantic's BaseModel is the core of the Pydantic Docs data validation library. By creating a class that inherits from BaseModel, you define a data structure using standard Python type hints. Pydantic then automatically validates incoming data, handles type conversions (coercion), and safely serializes it.

class TaskCreate(BaseModel):
    title: str



# What is a Schema?

# Think:

# Schema
# =
# Shape of incoming data

# We're telling FastAPI:

# I only accept:

# {
#     "title": "some text"
# }

# If someone sends:

# {
#     "name": "something"
# }

# FastAPI will reject it automatically.