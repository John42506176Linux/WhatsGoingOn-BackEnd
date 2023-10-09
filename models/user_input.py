from pydantic import BaseModel

# Define data model
class UserInput(BaseModel):
    location: str
    date: str