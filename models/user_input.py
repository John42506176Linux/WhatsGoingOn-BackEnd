from pydantic import BaseModel

# Define data model
class UserInput(BaseModel):
    location: str # City, State format (e.g. San Francisco, CA)
    date: str # YYYY-MM-DD format