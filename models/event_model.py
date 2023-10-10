from pydantic import BaseModel, Field
from typing import Optional

class Event(BaseModel):
    event_date: Optional[str] = Field(description="When is the event occuring given this tweet's publish date (YYYY-MM-DD)? Returns empty if it's the publish date.")
    event_link: str = Field(description="The RSVP link for the event")
    event_title: str = Field(description="The name of the event (e.g. PyCon)")
    event_location: Optional[str] = Field(description="The location of the event in City, State format")
    is_local: bool = Field(description="Whether the event is local to the user (e.g true, false)")
    is_tweet_event: bool = Field(description="Whether the tweet is about an upcoming event with an RSVP link (e.g true, false)")
    is_in_state: bool = Field(description="Whether the event is in the same state as the user (e.g true, false)")
    is_event_date_available: bool = Field(description="Whether the tweet contains the date of the event (e.g true, false)")
    is_location_available: bool = Field(description="Whether the tweet contains the location of the event (e.g true, false)")
    is_related_to_preference: bool = Field(description="Whether the tweet is related to the user's preference (e.g true, false)")

