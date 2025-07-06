import random
import time

import requests
from openai import OpenAI

# vllm
client1 = OpenAI(base_url=f'http://localhost:8881/v1/', api_key='sk-xxx')
clients = [client1]

def generate_response_vllm(llm_type='llama3', temperature=0, user_prompt=None, sys_prompt=None, api_key=''):
    response = None
    while response is None:
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
    response = response.choices[0].message.content.strip()  # ['content']
    messages.append({"role": "assistant", "content": response})
    return messages
