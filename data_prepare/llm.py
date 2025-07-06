import random
import time

import requests
from openai import OpenAI

# vllm
client1 = OpenAI(base_url=f'http://localhost:8881/v1/', api_key='sk-xxx')
client2 = OpenAI(base_url=f'http://localhost:8882/v1/', api_key='sk-xxx')
# clients = [client1, client2]
clients = [client2]

def generate_response_vllm(llm_type='llama3', temperature=0, user_prompt=None, sys_prompt=None, api_key=''):
    response = None
    cnt = 1
    start_time = time.time()  # Record the start time
    max_tokens = 30000
    time_limit = 120
    while response is None:
        elapsed_time = time.time() - start_time
        if elapsed_time >= time_limit:  # If time exceeds limit (60 seconds)
            print("Time limit exceeded, adjusting max_tokens.")
            max_tokens = 2048 
        client = clients[random.randint(0, len(clients) - 1)]
        try:
            if sys_prompt is not None:
                messages = [ 
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_prompt}
                ]
                response = client.chat.completions.create(
                    model=llm_type,
                    messages=messages,
                    temperature=temperature,
                )
            else:
                messages = [
                    {"role": "user", "content": user_prompt}
                ]
                response = client.chat.completions.create(
                    model=llm_type,
                    messages=messages,
                    temperature=temperature,
                )
        except Exception as e:
            print(e)
            cnt += 1
            if cnt >= 10:
                max_tokens = 2048
                print("Time limit exceeded, adjusting max_tokens.")
    response = response.choices[0].message.content.strip()  # ['content']
    messages.append({"role": "assistant", "content": response})
    return messages
