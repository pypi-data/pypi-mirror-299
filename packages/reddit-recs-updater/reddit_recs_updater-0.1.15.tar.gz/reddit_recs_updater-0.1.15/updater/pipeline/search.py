import asyncio
import re
from updater.utils.google_handler import fetch_google_results

# List of search terms -> Dict of google results data with unique submission ids as keys
async def search_reddit(search_terms: list[str], max_results: int) -> dict[str, dict]:
  unique_results_dict = {}
  
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
        if subm_id and subm_id not in unique_results_dict:
          unique_results_dict[subm_id] = {
            'title': item['title'],
            'snippet': item['snippet'],
            'link': item['link']
          }

  return unique_results_dict


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
    'best air fryer for large families'
  ]
  unique_results_dict = asyncio.run(search(search_terms, 10))
  print(unique_results_dict)