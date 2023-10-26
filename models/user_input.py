from pydantic import BaseModel
from typing import List

# Define data model
class UserInput(BaseModel):
    location: str # City, State format (e.g. San Francisco, CA)
    date: str # YYYY-MM-DD format
    event_preferences: List[str] # List of event preferences (e.g. ["Tech", "Art & Music"])