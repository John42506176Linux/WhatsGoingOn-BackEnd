from fastapi import FastAPI
import re
import json
from dotenv import load_dotenv
from models.user_input import UserInput
from models.event_model import Event
from langchain.output_parsers import PydanticOutputParser
from langchain.llms import OpenAI
from langchain.prompts import (
    PromptTemplate,
)
import datetime
load_dotenv()
from tools.metaphor_tools import search, get_twitter_contents
from langchain.output_parsers import PydanticOutputParser


# search = MetaphorSearchAPIWrapper()

# Initialize FastAPI app
app = FastAPI()

# Define endpoint
@app.post("/get_event")
async def get_events(data: UserInput,):
    # Use OpenAI to generate metaphor
    date_obj = datetime.datetime.strptime(data.date, '%Y-%m-%d')
    one_week_ago = date_obj - datetime.timedelta(days=7)
    parser = PydanticOutputParser(pydantic_object=Event)
    prompt = PromptTemplate(
        template="Extract the information from the user's tweet based on the date the tweet was published and the user's area {location}.\n{format_instructions}\nPublished Date:{publish_date}\nTweet:{tweet}",
        input_variables=["tweet","publish_date",],
        partial_variables={"format_instructions": parser.get_format_instructions(),
                           "location": data.location},
    )
    # Format the date as a string in YYYY-MM-DDTHH:MM:SSZ format
    formatted_date = one_week_ago.strftime('%Y-%m-%dT%H:%M:%SZ')

    text = search(f"Find me upcoming cool tech events in {data.location} occuring afer {data.date}.",formatted_date)
    
    contents = text.get_contents().contents
    publish_dates = [result.published_date for result in text.results]
    gpt_list = []

    for content,publish_date in zip(contents, publish_dates):
        input = get_twitter_contents(content.extract)
        _input = prompt.format_prompt(tweet=input,publish_date=publish_date)
        model = OpenAI(temperature=0,model_name="gpt-3.5-turbo-0613")
        output = model(_input.to_string())
        output = parser.parse(output).dict()
        output['url'] = content.url
        gpt_list.append(output)
    # Print content for each result
    return {"response" : json.dumps(gpt_list)}