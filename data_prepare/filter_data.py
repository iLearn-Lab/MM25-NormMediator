import os
import json
from tqdm import tqdm
import shutil

def filter_dialogue(data_size = 1000, round = 0):
    filter_id = []
    new_data = {}
    source_file = f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}/generate_dialogue.json"
    backup_file = f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}/generate_dialogue_backup.json"
    shutil.copy(source_file, backup_file)
    with open(source_file, 'r') as f:
        data = json.load(f)
        for k in tqdm(data.keys()):
            # if round > 2:
            #     agent_properties = results[i][k]['agent_description'][list(results[i][k]['agent_description'].keys())[0]].get('dynamic_properties', [])
            #     social_network = results[i][k].get('social_network', [])
            #     dialogue = results[i][k].get('dialogue', [])
            #     dialogue_norms = results[i][k].get('dialogue_norms', [])
            #     interaction_evaluation = results[i][k].get('interaction_evaluation', [])
            #     user_assessment = results[i][k].get('user_assessment', [])
            #     conflict_norms = results[i][k].get('conflict_norms', [])
            #     mediation_strategy = results[i][k].get('mediation_strategy', [])

            #     if len(agent_properties) != round or len(social_network) != round or len(dialogue) != round or len(dialogue_norms) != round-1  \
            #         or len(interaction_evaluation) != round-1  or len(user_assessment) != round-1  or len(conflict_norms) != round-1  or len(mediation_strategy) != round-1 :
            #         filter_id.append(k)
            #     print(f"Round {round}: {filter_id}")
            if not isinstance(results[i][k]['dialogue'], list):
                results[i][k]['dialogue'] = [results[i][k]['dialogue']]
            original_dialogue = results[i][k]['dialogue'][-1]
            try:
                speakers = [s['speaker'] for s in original_dialogue.values()]
            except:
                if 'speaker' in original_dialogue.keys():
                    speakers = [original_dialogue['speaker']]
                    round_id = original_dialogue['round_id']
                    del original_dialogue['round_id']
                    original_dialogue = {round_id: original_dialogue}
                # 定义需要检查的键名及其优先级顺序（按原代码顺序）
                keys_to_check = ['round_id', 'dialogue', 'meditation', 'mediator-dialogue', 'mediation_plan']
                # 按优先级检查键是否存在
                for key in keys_to_check:
                    if key in original_dialogue:
                        original_dialogue = original_dialogue[key]
                        break  # 找到后立即终止循环
                for entry in original_dialogue.values():
                    if ' speaker' in entry:  # 检查是否存在带空格的旧键
                        # 将旧键的值迁移到新键，并删除旧键
                        entry['speaker'] = entry.pop(' speaker')
                alter_dict = {}
                try:
                    for a, s in enumerate(original_dialogue.values()):
                        alter_dict[str(a + 1)] = s
                        if 'speaker' not in s.keys():
                            for ss in s:
                                speaker = list(s.keys())[0]  # 获取第一个键作为speaker
                                expression = s[speaker]["expression"]
                                action = s[speaker]["action"]
                                chat_content = s["chat_content"]
                                # 构造目标格式的数据
                                alter_dict[str(a + 1)] = {
                                    "speaker": speaker,
                                    "expression": expression,
                                    "action": action,
                                    "chat_content": chat_content
                                }
                    original_dialogue = alter_dict
                except Exception as e:
                    print(e) 
                    filter_id.append(k)
                    continue
                try:
                    speakers = [s['speaker'] for s in original_dialogue.values()]
                    results[i][k]['dialogue'] = original_dialogue
                except Exception as e:
                    print(e) 
                    filter_id.append(k)
                    continue
            if round != 0:
                if 'Mediator' not in speakers:
                    filter_id.append(k)
            results[i][k]['dialogue'][-1] = original_dialogue
        id_n = 0
        for k in tqdm(data.keys()):
            if k not in filter_id:
                new_data[id_n] = results[i][k]
                id_n += 1
        print(id_n)
        with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}/generate_dialogue.json", "w", encoding="utf8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
            
                
def all_data():    
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/filter_id_5.txt", 'r') as f:
        filter_id = [i.replace('\n', '') for i in f.readlines()]
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/1/mediation_strategy_generation.json", 'r') as f:
        data = json.load(f)
        for i in filter_id:
            del results[i][i]
        for i in data.keys():
            results[i][i]['dialogue'] = [results[i][i]['dialogue']]
            results[i][i]['interaction_evaluation'] = [results[i][i]['interaction_evaluation']]
            results[i][i]['user_assessment'] = [results[i][i]['user_assessment']]
            results[i][i]['conflict_norms'] = [results[i][i]['conflict_norms']]
            results[i][i]['mediation_strategy'] = [results[i][i]['mediation_strategy']]
            results[i][i]['social_network'] = [results[i][i]['social_network']]
            for k in results[i][i]['agent_description'].keys():
                results[i][i]['agent_description'][k]['dynamic_properties'] = [results[i][i]['agent_description'][k]['dynamic_properties']]
    for round in range(2,6):
        with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{data_size}/{round}/mediation_strategy_generation.json", 'r') as f:
            data_pre = json.load(f)
            for i in data.keys():
                results[i][i]['dialogue'].append(data_pre[i]['dialogue'])
                results[i][i]['interaction_evaluation'].append(data_pre[i]['interaction_evaluation'])
                results[i][i]['user_assessment'].append(data_pre[i]['user_assessment'])
                results[i][i]['conflict_norms'].append(data_pre[i]['conflict_norms'])
                results[i][i]['mediation_strategy'].append(data_pre[i]['mediation_strategy'])
                results[i][i]['social_network'].append(data_pre[i]['social_network'])
                for k in results[i][i]['agent_description'].keys():
                    results[i][i]['agent_description'][k]['dynamic_properties'].append(data_pre[i]['agent_description'][k]['dynamic_properties'])
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/conflict_mediation_{data_size}.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
def combine_data():   
    # data = {}
    data_path = []
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/conflict_mediation.json", 'r') as f:
        data = json.load(f)
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/conflict_mediation_{data_size}.json", 'r') as f:
        data_pre = json.load(f)
    result = {}
    i = 1
    for d in data.values():
        result[str(i)] = dict(d)
        i += 1
    for d in data_pre.values():
        result[str(i)] = dict(d)
        i += 1
    print(i)
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/conflict_mediation.json", "w", encoding="utf8") as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
def filter_data():
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/conflict_mediation.json", 'r') as f:
        data = json.load(f)
    result = {}
    i = 1
    for d in data.values():
        result[str(i)] = dict(d)
        i += 1    
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/conflict_mediation.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_size', type=int, default=100)
    parser.add_argument('--round', type=int, default=1)
    args = parser.parse_args()
    round = args.round
    data_size = args.data_size
    if round < 3:
        filter_dialogue(data_size = data_size, round = round)
    # all_data()
    # conbine_data()