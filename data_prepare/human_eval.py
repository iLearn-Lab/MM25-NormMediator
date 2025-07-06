import os
import json
from collections import defaultdict

# Base directory
base_dir = '/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/tag'

# Initialize a dictionary to collect sums and counts
sums = defaultdict(float)
counts = defaultdict(int)

# Recursively load all scenario_scores.json in subdirectories
for root, dirs, files in os.walk(base_dir):
    if 'scenario_scores.json' in files:
        file_path = os.path.join(root, 'scenario_scores.json')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

            for scenario in data.values():
                # Loop through each attribute
                for key, value in scenario.items():
                    if isinstance(value, int) or isinstance(value, float):
                        # Sum the values and count occurrences
                        sums[key] += value
                        counts[key] += 1
                    elif isinstance(value, list):
                        # Calculate average for list and treat it as a single value
                        if value:
                            average_value = sum(value) / len(value)
                            sums[key] += average_value
                            counts[key] += 1

# Calculate averages
averages = {key: sums[key] / counts[key] for key in sums}

# Output the results
for key, avg in averages.items():
    print(f"{key}: {avg:.2f}")