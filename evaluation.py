import json
import os
from collections import defaultdict
import numpy as np
import ast
import matplotlib.pyplot as plt
import numpy as np
import re

def process_single_round(round_num, data, metrics):
    # Process interaction evaluation metrics
    interaction = data.get('interaction_evaluation')[round_num]
    metrics['conflict_score'][round_num].append(interaction.get('conflict_level'))
    metrics['emotional_intensity'][round_num].append(interaction.get('emotional_intensity'))

    # Process user assessment metrics
    user_assess = data.get('user_assessment')[round_num]
    sat_values = []
    ep_values = []
    for u in user_assess.values():
        try:
            sat_values.append(float(u.get('satisfaction_level')))
        except:
            continue
        try:
            ep_values.append(float(u.get('emotional_pressure')))
        except:
            continue
    sat_mean = np.mean([u for u in sat_values if not (isinstance(sat_values, (int, float)) and np.isnan(sat_values))])
    ep_mean = np.mean([u for u in ep_values if not (isinstance(ep_values, (int, float)) and np.isnan(ep_values))])
    if not np.isnan(sat_mean):
        metrics['satisfaction'][round_num].append(sat_mean)
    if not np.isnan(ep_mean):
        metrics['emotional_pressure'][round_num].append(ep_mean)

    # Process social network weights
    weights = []
    numbers = re.findall(r'-?\d+\.\d+|-?\d+', str(data.get('social_network')[round_num+1]))
    weights = [float(num) for num in numbers]
    average_weight = np.mean(weights)
    count_cooperate = sum(1 for weight in weights if weight > 0)
    count_conflict = sum(1 for weight in weights if weight < 0)
    metrics['social_weights'][round_num].append(average_weight)
    metrics['cooperate_num'][round_num].append(count_cooperate)
    metrics['conflict_num'][round_num].append(count_conflict)

def generate_report(metrics, sorted_rounds):
    report = {}

    # Common statistical function
    def calculate_stats(values):
        result = []
        for value in values:
            numeric_values = [v for v in value if isinstance(v, (int, float))]
            result.append({
                'max': max(numeric_values),
                'min': min(numeric_values),
                'avg': sum(numeric_values)/len(numeric_values),
                'changes': calculate_changes(numeric_values)
            })
        return result

    def calculate_changes(values):
        changes = {'increase': 0, 'decrease': 0, 'same': 0}
        prev = None
        for v in values:
            if prev is not None:
                if v > prev: changes['increase'] += 1
                elif v < prev: changes['decrease'] += 1
                else: changes['same'] += 1
            prev = v
        return changes

    # Generate reports for each metric
    for metric in ['conflict_score', 'emotional_intensity', 'satisfaction', 'emotional_pressure']:
        values = [metrics[metric][r] for r in sorted_rounds]
        report[metric] = calculate_stats(values)

    social_report = {}
    for i in range(len(metrics['social_weights'])):
        social_report[sorted_rounds[i]] = np.mean(metrics['social_weights'][sorted_rounds[i]])
    report['social_network'] = social_report

    cooperate_num = {}
    for i in range(len(metrics['cooperate_num'])):
        cooperate_num[sorted_rounds[i]] = sum(metrics['cooperate_num'][sorted_rounds[i]])
    report['cooperate_num'] = cooperate_num

    conflict_num = {}
    for i in range(len(metrics['conflict_num'])):
        conflict_num[sorted_rounds[i]] = sum(metrics['conflict_num'][sorted_rounds[i]])
    report['conflict_num'] = conflict_num

    return report

if __name__ == "__main__":
    round_paths = [500, 1000, 2000]
    round = 6

    # Initialize data structure
    metrics = {
        'conflict_score': defaultdict(list),
        'emotional_intensity': defaultdict(list),
        'satisfaction': defaultdict(list),
        'emotional_pressure': defaultdict(list),
        'stress_level': defaultdict(lambda: defaultdict(list)),
        'social_weights': defaultdict(list),
        'cooperate_num': defaultdict(list),
        'conflict_num': defaultdict(list)
    }

    # Collect data for all rounds
    filename = f'{round}/user_assessment.json'
    data = {}
    i = 0
    for round_path in round_paths:
        with open(os.path.join(f'/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{round_path}', filename), 'r') as f:
            data0 = json.load(f)
            for j in data0.values():
                data[i] = j
                i += 1
        # Assume JSON structure is {round_num: data}, e.g., {"1": {}, "2": {}}

    for round_data in data.values():
        for round_num in range(round):
            process_single_round(round_num, round_data, metrics)

    # Sort rounds and generate report
    sorted_rounds = sorted(metrics['conflict_score'].keys(), key=int)
    analysis_report = generate_report(metrics, sorted_rounds)

    # Output example (can be formatted as JSON or table as needed)
    print("=== Interaction Analysis ===")
    print("1. Conflict Score")
    conflict_score = [float(f"{value['avg']:.2f}") for value in analysis_report['conflict_score']]
    print(conflict_score)
    print("2. Emotional Intensity")
    emotional_intensity = [float(f"{value['avg']:.2f}") for value in analysis_report['emotional_intensity']]
    print(emotional_intensity)

    print("=== Agent Interview ===")
    print("1. Satisfaction")
    satisfaction = [float(f"{value['avg']:.2f}") for value in analysis_report['satisfaction']]
    print(satisfaction)
    print("2. Emotional Pressure")
    emotional_pressure = [float(f"{value['avg']:.2f}") for value in analysis_report['emotional_pressure']]
    print(emotional_pressure)

    print("\n=== Social Network Weight Analysis ===")
    social_network = [float(f"{value:.2f}") for value in analysis_report['social_network'].values()]
    print(social_network)
    cooperate_num = [int(value) for value in analysis_report['cooperate_num'].values()]
    print(cooperate_num)
    conflict_num = [int(value) for value in analysis_report['conflict_num'].values()]
    print(conflict_num)
