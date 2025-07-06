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

def filter_data(original_dialogue, i):
    try:
        speakers = [s['speaker'] for s in original_dialogue.values()]
        expression = [s['expression'] for s in original_dialogue.values()]
        action = [s['action'] for s in original_dialogue.values()]
        chat_content = [s['chat_content'] for s in original_dialogue.values()]
        if 'Mediator' not in speakers:
            return False
        results[str(i)]['dialogue'].append(original_dialogue)
        return True
    except:
        if 'speaker' in original_dialogue.keys():
            speakers = [original_dialogue['speaker']]
            round_id = original_dialogue['round_id']
            del original_dialogue['round_id']
            original_dialogue = {round_id: original_dialogue}
        # Define the keys to be checked along with their priority order (in the original code sequence)
        keys_to_check = ['round_id', 'dialogue', 'meditation', 'mediator-dialogue', 'mediation_plan']
        # Check if the key exists according to the priority order
        for key in keys_to_check:
            if key in original_dialogue:
                original_dialogue = original_dialogue[key]
                break  # Terminate the loop immediately upon finding it.
        for entry in original_dialogue.values():
            if ' speaker' in entry:  # 检查是否存在带空格的旧键
                # Move the values of the old keys to the new keys and delete the old keys.
                entry['speaker'] = entry.pop(' speaker')
        alter_dict = {}
        try:
            pre_id = 1
            for a, s in enumerate(original_dialogue.values()):
                alter_dict[str(pre_id + a)] = s
                if 'speaker' not in s.keys():
                    for ss in s:
                        speaker = list(s.keys())[0]  # Obtain the first key as the speaker
                        expression = s[speaker]["expression"]
                        action = s[speaker]["action"]
                        chat_content = s["chat_content"]
                        # Construct data in the target format
                        alter_dict[str(pre_id + a)] = {
                            "speaker": speaker,
                            "expression": expression,
                            "action": action,
                            "chat_content": chat_content
                        }
            original_dialogue = alter_dict
        except Exception as e:
            print(e) 
            return False
        try:
            speakers = [s['speaker'] for s in original_dialogue.values()]
            results[str(i)]['dialogue'].append(original_dialogue)
            return True
        except Exception as e:
            print(e) 
            return False
    
def run(i):
    results[str(i)]['dialogue'] = results[str(i)]['dialogue'] if isinstance(results[str(i)]['dialogue'], list) else [results[str(i)]['dialogue']]
    while True:
        try:
            agent_description = {}
            for person, attributes in agent_description.items():
                # If dynamic_properties is a list, take the last element.
                if isinstance(attributes['dynamic_properties'], list):
                    attributes['dynamic_properties'] = attributes['dynamic_properties'][-1]
                # Retain each person's attribute value in the dictionary
                agent_description[person] = attributes
            sys_prompt, user_prompt = mediation_interaction(results[i]['situation_description'], agent_description, results[i]['social_network'][-1], results[i]['dialogue'][-1], results[i]['conflict_norms'][-1])
            result = generate_response_vllm(sys_prompt=sys_prompt , user_prompt=user_prompt, temperature=1)
            match = re.search(r"\{.*\}", result[-1]['content'], re.DOTALL)  # `re.DOTALL` enables `.` to match newline characters.
            if match:
                extracted_dict_str = match.group()  # Extract the dictionary string that matches.
                try:
                    # Parse the string into a dictionary
                    extracted_dict = ast.literal_eval(extracted_dict_str)
                    json.dumps(extracted_dict)
                    if filter_data(extracted_dict, i):
                        # results[str(i)]['dialogue'].append(extracted_dict)
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
    parser.add_argument('--data_size', type=int, default=100)
    parser.add_argument('--round', type=int, default=1)
    args = parser.parse_args()
    data_size = args.data_size
    round = args.round
    o_dir = Path(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}")
    o_dir.mkdir(exist_ok=True)
    input_file = o_dir / 'norm_mediation.json'
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
    
