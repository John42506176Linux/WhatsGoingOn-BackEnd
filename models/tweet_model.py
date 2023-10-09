from pydantic import Field
from models.event_model import Event

class TweetEvent(Event):
    retweet_count: int = Field(description="The number of retweets")
    favorite_count: int = Field(description="The number of favorites(likes)")
    reply_count: int = Field(description="The number of replies")

    @classmethod
    def fromEvent(cls, event: Event, retweet_count: int, favorite_count: int, reply_count: int):
        dict = event.dict()
        dict['retweet_count'] = retweet_count
        dict['favorite_count'] = favorite_count
        dict['reply_count'] = reply_count
        return cls(**dict)