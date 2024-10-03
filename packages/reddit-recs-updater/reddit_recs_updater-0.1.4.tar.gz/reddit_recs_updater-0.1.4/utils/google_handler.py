import asyncio
import aiohttp
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional

load_dotenv()

google_search_engine_id = os.environ['google_searchengine_id']
google_api_key = os.environ['google_api_key']

async def fetch_google_results(search_query: str, search_site: str, search_range_days: Optional[int], max_results: int) -> List[Dict[str, str]]:
  # each call returns 10 results
  if search_range_days:
    date_restriction = f'd{search_range_days}'
  else:
    date_restriction = ""
  
  results_fetched = 0
  start_index = 1
  all_items = []

  async with aiohttp.ClientSession() as session:
    while results_fetched < max_results:
      # Construct api call url with parameters
      url = f"https://www.googleapis.com/customsearch/v1?q={search_query}&cx={google_search_engine_id}&key={google_api_key}&dateRestrict={date_restriction}&siteSearch={search_site}&siteSearchFilter=i&start={start_index}"

      async with session.get(url) as response:
        data = await response.json()

      items = data.get('items', [])
      all_items.extend(items)

      results_fetched += len(items)
      start_index += len(items)

      # Break if no more results are returned
      if not items:
        break

  return all_items[:max_results]

# For testing purposes
if __name__ == "__main__":
  search_query = "best M2 Max"
  search_site = "reddit.com"
  search_range_days = None
  max_results = 10

  results = asyncio.run(fetch_google_results(search_query, search_site, search_range_days, max_results))
  # pp.pprint(results)
  for result in results:
    print(result['title'])
    print(result['snippet'])
    print("\n")
  
  