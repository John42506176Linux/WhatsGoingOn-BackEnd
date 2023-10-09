from pydantic import BaseModel, Field
from typing import Optional

class Event(BaseModel):
    event_date: Optional[str] = Field(description="When is the event occuring given this tweet's publish date (YYYY-MM-DD)? Returns empty if it's the publish date.")
    event_link: str = Field(description="The RSVP link for the event")
    event_name: str = Field(description="The name of the event (e.g. PyCon)")
    event_location: Optional[str] = Field(description="The location of the event in City, State format")
    is_local: bool = Field(description="Whether the event is local to the user")
    is_tweet_event: bool = Field(description="Whether the tweet is about an upcoming event with an RSVP link")
    is_in_state: bool = Field(description="Whether the event is in the same state as the user")
    is_event_date_available: bool = Field(description="Whether the tweet contains the date of the event")
    is_location_available: bool = Field(description="Whether the tweet contains the location of the event")

