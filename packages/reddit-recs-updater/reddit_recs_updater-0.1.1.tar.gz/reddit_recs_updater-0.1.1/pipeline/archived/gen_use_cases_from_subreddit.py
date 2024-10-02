import json
from utils.ai_handler import get_openai_response

async def gen_use_cases_from_subreddit(submission, product_category, use_cases) -> list[str]:
  
  # Get subreddit info from submission
  subreddit = submission.subreddit
  subreddit_name = subreddit.display_name
  subreddit_description = subreddit.public_description

  # Ask LLM to generate use cases
  sys_prompt = open('llm_prompts/gen_use_cases_subreddit_sys.txt', 'r').read()
  user_prompt = f"Product: {product_category}\nSubreddit name: {subreddit_name}\nSubreddit description: {subreddit_description}\nPossible use cases: {use_cases}"
  model = 'gpt-4o-2024-08-06'
  response_format = { "type": "json_object" }

  openai_response = await get_openai_response(sys_prompt, user_prompt, model, response_format, 'gen_use_cases_from_subreddit')

  return openai_response['use_cases']