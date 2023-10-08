from metaphor_python import Metaphor
from langchain.tools import tool
from typing import List
import os

# Configure OpenAI with your API key
metaphor = Metaphor(api_key=os.environ["METAPHOR_API_KEY"])

@tool
def search(query: str):
    """Call search engine with a query."""
    return metaphor.search(query,include_domains=["twitter.com"],
    start_published_date="2023-09-01",num_results=10)

@tool
def get_contents(ids: List[str]):
    """Get contents of a webpage.
    
    The ids passed in should be a list of ids as fetched from `search`.
    """
    content_list = []
    contents = metaphor.get_contents(ids).contents
    for content in contents:
        content_dict = {
            "url" : content.url,
            "content" : content.extract.split('</div>')[0 ],
        }
        content_list.append(content_dict)

    return content_list

@tool
def find_similar(url: str):
    """Get search results similar to a given URL.
    
    The url passed in should be a URL returned from `search`
    """
    return metaphor.find_similar(url, num_results=10)