import os
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv(override=True)
key = os.getenv("TAVILY_API_KEY")
print("Key loaded:", bool(key), "| starts with tvly-:", str(key).startswith("tvly-"))

client = TavilyClient(api_key=key)
res = client.search(query="latest Python version", max_results=3)
for r in res["results"]:
    print(r["url"])