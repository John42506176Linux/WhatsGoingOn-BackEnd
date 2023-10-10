from fastapi import FastAPI
import json
from dotenv import load_dotenv
from models.user_input import UserInput
from models.event_model import Event
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    PromptTemplate,
)
import datetime
load_dotenv()
from tools.metaphor_tools import search
from tools.twitter_tools import process_batch_tweets

# Initialize FastAPI app
app = FastAPI()

# Define endpoint
@app.post("/get_event")
async def get_events(data: UserInput,):
    # Define prompt template to extract information from events
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

    # Call search engine with a query
    text = search(f"Find me upcoming cool tech events in {data.location} occuring afer {data.date}.",formatted_date)
    
    # Get contents and publish dates from search results
    contents = text.get_contents().contents
    publish_dates = [result.published_date for result in text.results]
    gpt_list = []
    
    # Processes tweets to json
    process_batch_tweets(contents,publish_dates,parser,prompt,gpt_list)
    # Print content for each result
    return {"response" : json.dumps(gpt_list,indent=4)}