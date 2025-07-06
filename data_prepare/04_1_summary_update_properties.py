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

def extract_valid_dict(content):
    """Extract the JSON string from the text and parse it into a dictionary."""
    match = re.search(r"\{.*\}", content, re.DOTALL)
    if match:
        try:
            extracted_dict = ast.literal_eval(match.group())
            json.dumps(extracted_dict)  # 验证 JSON 格式
            return extracted_dict
        except Exception:
            return None
    return None

def update_results(i, extracted_dict):
    """Update the "results" dictionary"""
    state_ok, network_ok = False, False
    if not extracted_dict:
        return state_ok, network_ok

    if 'state_update' in extracted_dict and 'social_network_update' in extracted_dict:
        # Update social network information
        if 'nodes' in extracted_dict['social_network_update'] and 'edges' in extracted_dict['social_network_update']:
            results[str(i)]['social_network'] = results[str(i)]['social_network'] if isinstance(results[str(i)]['social_network'], list) else [results[str(i)]['social_network']]
            results[str(i)]['social_network'].append(extracted_dict['social_network_update'])
            network_ok = True

        # Update the status information of the agent
        if all({'stress_level', 'behavior', 'memory'}.issubset(i) for i in extracted_dict['state_update'].values()):
            for k in results[str(i)]['agent_description'].keys():
                state_data = extracted_dict['state_update'].get(k, {})
                results[str(i)]['agent_description'][k]['dynamic_properties'] = results[str(i)]['agent_description'][k]['dynamic_properties'] if isinstance(results[str(i)]['agent_description'][k]['dynamic_properties'], list) else [results[str(i)]['agent_description'][k]['dynamic_properties']]
                results[str(i)]['agent_description'][k]['dynamic_properties'].append(state_data)
            state_ok = True

    return state_ok, network_ok

def run(i):
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
            results[i]['dialogue'] = results[i]['dialogue'] if isinstance(results[i]['dialogue'], list) else [results[i]['dialogue']]
            sys_prompt, user_prompt = summary_update_properties2(
                results[i]['dialogue'][-1], agent_description, results[i]['social_network'][-1]
            )
            all_results = generate_response_vllm(sys_prompt=sys_prompt, user_prompt=user_prompt, temperature=1)

            # Parse the complete JSON
            extracted_dict = extract_valid_dict(all_results[-1]['content'])
            state_ok, network_ok = update_results(i, extracted_dict)

            if state_ok and network_ok:
                break

            # Handle multi-part return
            all_results_split = [d for d in all_results[-1]['content'].split('##') if d.strip()]
            for result in all_results_split:
                extracted_dict = extract_valid_dict(result)
                state_ok, network_ok = update_results(i, extracted_dict)
                if state_ok and network_ok:
                    break

        except Exception as e:
            print(e)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_size', type=int, default=1000)
    parser.add_argument('--round', type=int, default=1)
    args = parser.parse_args()
    data_size = args.data_size
    round = args.round
    o_dir1 = Path(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round-1}")
    o_dir2 = Path(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}")
    o_dir2.mkdir(exist_ok=True)
    input_file = o_dir1 / 'generate_dialogue.json'
    output_file = o_dir2 / 'summary_update_properties.json' 
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
    
