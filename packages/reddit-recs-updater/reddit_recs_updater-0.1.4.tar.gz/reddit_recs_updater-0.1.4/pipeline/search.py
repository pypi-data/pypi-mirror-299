import asyncio
from utils.reddit_handler import search_reddit, get_subm_from_subm_id
from utils.google_handler import fetch_google_results
from asyncpraw.models import Submission

# List of search terms -> List of unique submission objects
async def search(search_terms: list[str], max_results: int) -> list[Submission]:
  unique_subms = {}
  
  # # Search Reddit
  # search_reddit_tasks = [
  #   asyncio.create_task(search_reddit(search_term, max_results, time_range="year", reddit_search_sort="relevance"))
  #   for search_term in search_terms
  # ]  
  # search_reddit_task_results = await asyncio.gather(*search_reddit_tasks)
  
  # for reddit_results in search_reddit_task_results:
  #   unique_subms.update({result.id: result for result in reddit_results})
  
  # Search Google
  search_site = "reddit.com"
  search_range_days_list = [365, 120, 60]
  search_google_tasks = [
    asyncio.create_task(fetch_google_results(search_term, search_site, search_range_days, max_results))
    for search_term in search_terms
    for search_range_days in search_range_days_list
  ]
  search_google_task_results = await asyncio.gather(*search_google_tasks)
  for result_set in search_google_task_results:
    for item in result_set:
      if 'link' in item:
        subm_id = item['link'].split('/')[-3]
        subm = await get_subm_from_subm_id(subm_id)
        if subm:
          unique_subms[subm.id] = subm

  return list(unique_subms.values())

if __name__ == "__main__":
  search_terms = ["Travel monitor macbook pro "]
  max_results = 5
  results = asyncio.run(search(search_terms, max_results))
  for subm in results:
    print(subm.title)
    print(subm.url)
    print(subm.id)
    print("\n")