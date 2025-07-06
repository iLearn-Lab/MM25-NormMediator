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

def validate_format(data):
    # Check if the main keys are present
    expected_main_keys = ["situation_description", "agent_description", "social_network"]
    for key in expected_main_keys:
        if key not in data:
            print(f"Missing key: {key}")
            return False
    agent_desc = data["agent_description"]
    if not isinstance(agent_desc, dict):
        return False
    for agent, properties in agent_desc.items():
        if not isinstance(properties, dict):
            return False
        expected_agent_keys = ["dynamic_properties"]
        for key in expected_agent_keys:
            if key not in properties:
                print(f"Missing key in agent {agent}: {key}")
                return False
        if "dynamic_properties" in properties:
            dynamic_props = properties["dynamic_properties"]
            if not isinstance(dynamic_props, dict):
                print(f"'dynamic_properties' for agent {agent} is not a dictionary.")
                return False
            if "stress_level" not in dynamic_props or "behavior" not in dynamic_props:
                print(f"Missing keys in 'dynamic_properties' for agent {agent}.")
                return False
            if not isinstance(dynamic_props["stress_level"], int):
                print(f"Incorrect type for 'stress_level' in agent {agent}: Expected int, got {type(dynamic_props['stress_level'])}")
                return False
            if not isinstance(dynamic_props["behavior"], str):
                print(f"Incorrect type for 'behavior' in agent {agent}: Expected str, got {type(dynamic_props['behavior'])}")
                return False
            
    return True

def run(i):
    while True:
        if str(i) in results.keys(): break
        sys_prompt, user_prompt = situation_agent()
        result = generate_response_vllm(sys_prompt=sys_prompt , user_prompt=user_prompt, temperature=1)
        match = re.search(r"\{.*\}", result[-1]['content'], re.DOTALL)  # `re.DOTALL` enables `.` to match newline characters.
        if match:
            extracted_dict_str = match.group()  # Extract the dictionary string that matches.
            try:
                # Parse the string into a dictionary
                extracted_dict = ast.literal_eval(extracted_dict_str)
                if validate_format(extracted_dict):
                    results[str(i)] = extracted_dict               
                    break
            except Exception as e:
                print(e)
                continue
        else:
            continue

if __name__ == "__main__":    
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_size', type=int, default=500)
    parser.add_argument('--round', type=int, default=0)
    args = parser.parse_args()
    data_size = args.data_size
    round = args.round
    o_dir = Path(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}")
    o_dir.mkdir(parents=True, exist_ok=True)
    output_file = o_dir / 'situation_agent.json' 
    datas = range(data_size)
    with ThreadPoolExecutor(max_workers=64) as executor:
        futures = []
        for i, data in enumerate(datas):
            futures.append(executor.submit(run, i))
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing tasks"):
            try:
                future.result()
            except Exception as e:
                print(f"Exception occurred: {e}")
        with(output_file).open("w", encoding="utf8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)
