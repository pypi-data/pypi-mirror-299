import asyncio
import re
from updater.utils.google_handler import fetch_google_results

# List of search terms -> List of unique submission ids
async def search(search_terms: list[str], max_results: int) -> list[str]:
  unique_subms_ids = []
  
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
        subm_id = extract_submission_id(item['link'])
        if subm_id and subm_id not in unique_subms_ids:
          unique_subms_ids.append(subm_id)

  return unique_subms_ids

def extract_submission_id(url):
  # Regular expression to match Reddit submission URLs
  pattern = r'https?://(?:www\.)?reddit\.com/r/\w+/comments/(\w+)/'
  match = re.match(pattern, url)

  if match:
    return match.group(1)
  else:
    return None


if __name__ == "__main__":
  search_terms = [
    'best air fryer for large families',
    'best air fryer for batch cooking'
  ]
  searched_subm_ids = asyncio.run(search(search_terms, 10))
  print(searched_subm_ids)
  print(len(searched_subm_ids))