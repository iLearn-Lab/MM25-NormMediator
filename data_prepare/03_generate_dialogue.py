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

def filter_data(original_dialogue):
    try:
        speakers = [s['speaker'] for s in original_dialogue.values()]
        expression = [s['expression'] for s in original_dialogue.values()]
        action = [s['action'] for s in original_dialogue.values()]
        chat_content = [s['chat_content'] for s in original_dialogue.values()]
        return True
    except:
        return False
        
def run(i):
    results[i] = datas[i]
    while True:
        try:
            agent_description = {}
            for person, attributes in agent_description.items():
                # If dynamic_properties is a list, take the last element.
                if isinstance(attributes['dynamic_properties'], list):
                    attributes['dynamic_properties'] = attributes['dynamic_properties'][-1]
                # Retain each person's attribute value in the dictionary
                agent_description[person] = attributes
            results[i]['social_network'] = results[i]['social_network'] if isinstance(results[i]['social_network'], list) else [results[i]['social_network']]
            sys_prompt, user_prompt = generate_dialogue(results[i]['situation_description'], agent_description, results[i]['social_norms_content'], results[i]['personal_norms_content'], results[i]['social_network'][-1])
            result = generate_response_vllm(sys_prompt=sys_prompt , user_prompt=user_prompt, temperature=1)
            match = re.search(r"\{.*\}", result[-1]['content'], re.DOTALL)  # `re.DOTALL` enables `.` to match newline characters.
            if match:
                extracted_dict_str = match.group()  # Extract the dictionary string that matches.
                try:
                    # Parse the string into a dictionary
                    extracted_dict = ast.literal_eval(extracted_dict_str)
                    json.dumps(extracted_dict)
                    if filter_data(extracted_dict):
                        results[str(i)]['dialogue'] = extracted_dict
                        break
                except Exception as e:
                    print(e)
                    continue
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_size', type=int, default=10)
    parser.add_argument('--round', type=int, default=0)
    args = parser.parse_args()
    data_size = args.data_size
    round = args.round
    o_dir = Path(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}")
    o_dir.mkdir(parents=True, exist_ok=True)
    input_file = o_dir / 'initialize_personal_norm.json'
    output_file = o_dir / 'generate_dialogue.json' 
    with open(input_file, "r", encoding="utf-8") as f:
        datas = json.load(f)
        results = datas
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
            
