# Given a subm, check if it has opinions. If yes, return subm data. Else, return none.
import json
from utils.ai_handler import get_openai_response_struct
from pydantic import BaseModel
from typing import Optional

async def scan_if_has_opns(subm_data: dict, pd_category_name: str) -> bool:
  print('- Checking if submission has opinions')
  
  class Inference(BaseModel):
    verbatim: Optional[str]
    product_brand: Optional[str]
    product_model_or_name: Optional[str]
    product_series: Optional[str]
    product_url: Optional[str]
    valid_rec_or_antirec: Optional[bool]
    
  sys_prompt_path = "llm_prompts/has_opn_sys.txt"
  with open(sys_prompt_path, "r") as file:
    sys_prompt = file.read()
  max_tokens_reddit = 3000
  reddit_thread_str = json.dumps(subm_data, indent=2)[:max_tokens_reddit * 4]
  user_prompt = f"I am shopping for a {pd_category_name}. Help me analyze this Reddit thread and determine if it has any recommendations or anti-recommendations for any brand, model or series for a {pd_category_name}.\n\n'Reddit Thread:'\n{reddit_thread_str}"
  model = "gpt-4o-mini"
  response_format = Inference

  response = await get_openai_response_struct(sys_prompt, user_prompt, model, response_format, 'has_opns')

  if response:
    verbatim = response.verbatim
    has_opn_raw = response.valid_rec_or_antirec
    has_pd_raw = response.product_brand or response.product_model_or_name or response.product_series or response.product_url
    has_opn = True if (has_opn_raw and has_pd_raw) else False

    print(f'- 1 Opinion extracted: {verbatim}')
    print(f'- 1 Product extracted: {has_pd_raw}')
    print(f'- LLM inference of validity: {has_opn_raw}')
    print(f'--> Has opinion?: {has_opn}')
    return has_opn
  else:
    return False
  

  
  