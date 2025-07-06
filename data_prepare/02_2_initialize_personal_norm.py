from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import sys
import os
# Get the current folder path.
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the current folder to sys.path
sys.path.append(current_dir)
from prompts import *
from llm import generate_response_vllm
from tqdm import tqdm
import json
import re
import ast

results= {}

def run(i):
    while True:
        sys_prompt, user_prompt = initialize_personal_norm(results[i]['situation_description'], results[i]['agent_description'])
        result = generate_response_vllm(sys_prompt=sys_prompt , user_prompt=user_prompt, temperature=1)
        match = re.search(r"\{.*\}", result[-1]['content'], re.DOTALL)  # `re.DOTALL` enables `.` to match newline characters.
        if match:
            extracted_dict_str = match.group()  # Extract the dictionary string that matches.
            try:
                # Parse the string into a dictionary
                extracted_dict = ast.literal_eval(extracted_dict_str)
                results[str(i)]['personal_norms_content'] = [d['content'] for d in extracted_dict.values()]
                results[str(i)]['personal_norms'] = extracted_dict
                break
            except Exception as e:
                print(e)
                continue
        else:
            continue

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_size', type=int, default=100)
    parser.add_argument('--round', type=int, default=1)
    args = parser.parse_args()
    data_size = args.data_size
    round = args.round
    o_dir = Path(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}")
    o_dir.mkdir(parents=True, exist_ok=True)
    input_file = o_dir / 'initialize_social_norm.json'
    output_file = o_dir / 'initialize_personal_norm.json'
    with open(input_file, "r", encoding="utf-8") as f:
        datas = json.load(f)
        results = datas
    if os.path.exists(output_file):
        with open(output_file, 'r', encoding='utf8') as f:
            results = json.load(f)
    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = []
        for i in datas.keys():
            futures.append(executor.submit(run, i))
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing tasks"):
            try:
                future.result()
            except Exception as e:
                print(f"Exception occurred: {e}")
        with(output_file).open("w", encoding="utf8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
