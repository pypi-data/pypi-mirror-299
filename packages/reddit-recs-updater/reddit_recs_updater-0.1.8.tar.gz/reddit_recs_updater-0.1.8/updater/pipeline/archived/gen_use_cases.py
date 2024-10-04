import json
from updater.utils.ai_handler import get_openai_response

# Product category (str) -> Dict of use cases (dict)
async def gen_use_cases(product_category: str) -> tuple[dict, list[str]]:
  print(f'Generating use cases for {product_category}...')

  model = 'gpt-4o-2024-08-06'
  response_format = { "type": "json_object" }
  with open('updater/llm_prompts/gen_use_cases_sys.txt', 'r') as file:
    sys_prompt = file.read()
  with open('updater/llm_prompts/gen_use_cases_user.txt', 'r') as file:
    user_prompt = file.read()
  user_prompt = user_prompt.replace('{product_category}', product_category)
  response = await get_openai_response(sys_prompt, user_prompt, model, response_format, 'gen_use_cases')
  
  use_cases_dict = response['Usage scenarios']
  use_cases_names = list(use_cases_dict.keys())

  print(json.dumps(use_cases_dict, indent=2))
  print(f'--> Use cases generated: {use_cases_names}')
  
  return use_cases_dict, use_cases_names