from metaphor_python import Metaphor
from langchain.tools import tool
from typing import List
import os
# Configure OpenAI with your API key
metaphor = Metaphor(api_key=os.environ["METAPHOR_API_KEY"])

def search(query: str,start_date: str):
    """Call search engine with a query."""
    try: 
        return metaphor.search(query,include_domains=["twitter.com"],
        start_published_date=start_date,num_results=10,use_autoprompt=True)
    except Exception as e:
        print(f"Error Searching:{e}")
        return None