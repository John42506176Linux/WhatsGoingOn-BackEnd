from metaphor_python import Metaphor
from langchain.tools import tool
from typing import List
import os
# Configure OpenAI with your API key
metaphor = Metaphor(api_key=os.environ["METAPHOR_API_KEY"])

def search(query: str,start_date: str):
    """Call search engine with a query."""
    return metaphor.search(query,include_domains=["twitter.com"],
    start_published_date=start_date,num_results=10,use_autoprompt=True)

def get_twitter_contents(extract: str):
    return extract.split('| created_at')[0].replace("<div>", "", 1)

# @tool
# def is_current_date(date: str, requested_date: str):
#     """
#     Check if event date is after requested date in initial query.

#     Date and requested date should be in the format YYYY-MM-DD.
#     """

#     # Convert the date strings to datetime objects
#     date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
#     requested_date_obj = datetime.datetime.strptime(requested_date, '%Y-%m-%d')

#     # Compare the datetime objects
#     return date_obj > requested_date_obj