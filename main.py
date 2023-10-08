from fastapi import FastAPI
import re
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.agent_token_buffer_memory import AgentTokenBufferMemory
import json
from dotenv import load_dotenv
from tools.metaphor_tools import search, get_contents, find_similar
from models.user_input import UserInput

load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Define endpoint
@app.post("/generate-event")
async def generate_metaphor(data: UserInput,):
    # Use OpenAI to generate metaphor
    system_message = SystemMessage(content="""
                                   You are a helpful event finder assistant who shows people popular upcoming events in the area based on the tweets, 
                                   you tell them them the tweets in the following format.
                                   Tweet by [twitter username]:
                                    - Event: [event name]
                                    - Date: [event date]
                                    - Link: [event link]
                                    - [Tweet Link]
                                   """)
    tools = [search, get_contents, find_similar]
    llm = ChatOpenAI(temperature=0.0)
    prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    memory_key = "history"

    memory = AgentTokenBufferMemory(memory_key=memory_key, llm=llm)
    agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory,
                                   return_intermediate_steps=True,verbose=True)
    result = agent_executor({"input":  f"Find me tweets about upcoming cool tech events in {data.location} occuring AFTER October 6th, 2023 at least 5 .",})
    text = result['output']
    
    
    # We first define the patterns that we will use to extract the data from the text
    # The patterns are used to match the specific lines in the text that hold the data we want to extract
    event_pattern = r"- Event: (.*?)\n"
    date_pattern = r"- Date: (.*?)\n"
    link_pattern = r"- Link: \[.*?\]\((.*?)\)"
    tweet_link_pattern = r"- \[Tweet Link\]\((.*?)\)"
    tweet_by_pattern = r"Tweet by (\w+):"

    
    # We use the re.findall() function to extract all occurrences of the pattern in the text
    # The findall() function returns a list of all matches of the pattern in the string
    
    tweet_by = re.findall(tweet_by_pattern, text)
    events = re.findall(event_pattern, text)
    dates = re.findall(date_pattern, text)
    links = re.findall(link_pattern, text)
    tweet_links = re.findall(tweet_link_pattern, text)
    
    # We initialize an empty list that will hold our data
    # This list will contain dictionaries, where each dictionary represents one tweet
    data = []
    
    # We iterate over the length of the tweet_by list. We use the length of the tweet_by list because it is the first list we created, but we could use the length of any of the lists
    # This loop will run as many times as there are tweets in the text
    for i in range(len(tweet_by)):
        # We use a try-except block to handle the case where the index i is out of range for one of the lists
        # This can happen if one of the data points is missing for a tweet
        try:
            tweet_by_val = tweet_by[i]
        except IndexError:
            tweet_by_val = ""
        try:
            event_val = events[i]
        except IndexError:
            event_val = ""
        try:
            date_val = dates[i]
        except IndexError:
            date_val = ""
        try:
            link_val = links[i]
        except IndexError:
            link_val = ""
        try:
            tweet_link_val = tweet_links[i]
        except IndexError:
            tweet_link_val = ""
        # We create a dictionary with the data for one tweet and append it to the data list
        # The dictionary contains five key-value pairs, where the keys are the names of the data points and the values are the extracted data
        data.append({
            "Tweet By": tweet_by_val,
            "Event": event_val,
            "Date": date_val,
            "Link": link_val,
            "Tweet Link": tweet_link_val
        })
    
    # We use the json.dumps() function to convert the list of dictionaries to a JSON string. The indent parameter is set to 4 to format the string in a more readable way
    json_data = json.dumps(data, indent=4)

    # Print content for each result
    return {"response" : json_data }