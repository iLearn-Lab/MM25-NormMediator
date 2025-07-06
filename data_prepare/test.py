import os
import json
from tqdm import tqdm

def delete_data():
    new_data = {}
    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/2000/0/situation_agent.json", 'r') as f:
        data = json.load(f)
        new_id = 0
        for k in tqdm(data.keys()):
            if int(k) > 999:
                new_data[str(new_id)] = results[i][k]
                new_id += 1

    with open(f"/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/1000/0/situation_agent.json", "w", encoding="utf8") as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
       
if __name__ == "__main__":
    delete_data()