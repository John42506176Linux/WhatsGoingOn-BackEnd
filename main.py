from fastapi import FastAPI, HTTPException
import json
from dotenv import load_dotenv
from models.user_input import UserInput
from models.event_model import Event,mockEvent
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    PromptTemplate,
)
import datetime
import os
load_dotenv()
from tools.metaphor_tools import search,MetaphorError
from tools.twitter_tools import process_batch_tweets

# Initialize FastAPI app
app = FastAPI()

# Define endpoint
@app.post("/get_event")
async def get_events(data: UserInput,):
    # Mock data for testing
    if os.environ["IS_TESTING"] == "True":
        return {"response": json.dumps([
            mockEvent,
            mockEvent,
            mockEvent,
            mockEvent,
            mockEvent,
            mockEvent,
        ])}
    parser = PydanticOutputParser(pydantic_object=Event)
    prompt = PromptTemplate(
        template="Extract the information from the user's tweet based on the date the tweet was published and the user's area {location}.\n The user's preference is {preference}\n{format_instructions}\nPublished Date:{publish_date}\nTweet:{tweet}",
        input_variables=["tweet","publish_date","preference"],
        partial_variables={"format_instructions": parser.get_format_instructions(),
                           "location": data.location},
    )

    # Format the date as a string in YYYY-MM-DDTHH:MM:SSZ format
    date_obj = datetime.datetime.strptime(data.date, '%Y-%m-%d')
    one_week_ago = date_obj - datetime.timedelta(days=7)
    formatted_date = one_week_ago.strftime('%Y-%m-%dT%H:%M:%SZ')
    event_preferences = " ".join(data.event_preferences)

    # Call search engine with a query
    text = search(f"Find me upcoming cool {event_preferences} events in {data.location} occuring afer {data.date}.",formatted_date)
    
    if(text is MetaphorError.RATE_LIMIT_EXCEEDED):
        raise HTTPException(status_code= 429,detail = f"Metaphor API Error: {text.value}")
    # Get contents and publish dates from search results
    contents = text.get_contents().contents
    publish_dates = [result.published_date for result in text.results]
    gpt_list = []
    
    # Processes tweets to json
    process_batch_tweets(contents,publish_dates,parser,prompt,gpt_list)
    # Print content for each result
    return {"response" : json.dumps(gpt_list)}