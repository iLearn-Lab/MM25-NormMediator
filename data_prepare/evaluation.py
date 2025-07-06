import json
import os
from collections import defaultdict
import numpy as np
import ast
import matplotlib.pyplot as plt
import numpy as np
import re

def process_single_round(round_num, data, metrics):
    # 处理交互评估指标
    interaction = data.get('interaction_evaluation')[round_num]
    metrics['conflict_score'][round_num].append(interaction.get('conflict_level'))
    metrics['emotional_intensity'][round_num].append(interaction.get('emotional_intensity'))

    # 处理用户评估指标
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
    # 处理社交网络权重
    weights = []
    numbers = re.findall(r'-?\d+\.\d+|-?\d+', str(data.get('social_network')[round_num+1]))
    weights = [float(num) for num in numbers]
    # for edge in data.get('social_network')[round_num+1].get('edges'):
    #     if isinstance(edge, str):
    #         # 将字符串转换为字典
    #         edge = ast.literal_eval(edge)
    #     if isinstance(edge, dict) and 'weight' in edge:
    #         weight = float(edge['weight'])
    #         weights.append(weight)
    average_weight = np.mean(weights)
    count_cooperate = sum(1 for weight in weights if weight > 0)
    count_conflict = sum(1 for weight in weights if weight < 0)
    metrics['social_weights'][round_num].append(average_weight)
    metrics['cooperate_num'][round_num].append(count_cooperate)
    metrics['conflict_num'][round_num].append(count_conflict)

def generate_report(metrics, sorted_rounds):
    report = {}
    
    # 通用统计函数
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

    # 生成各指标报告
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

def draw_pic(conflict_score, emotional_intensity, satisfaction, emotional_pressure, social_network, cooperate_num, conflict_num):
    plt.rcParams['font.family'] = 'Times New Roman'
    # 横坐标
    x = np.arange(len(conflict_score))
    
    # 使用 colormap 生成配色方案
    cm_r = plt.get_cmap('coolwarm')  
    cm = plt.get_cmap('cividis')      
    cm_g = plt.get_cmap('viridis')   
    
    # 创建水平子图（4列）
    fig, axs = plt.subplots(1, 4, figsize=(20, 4.5), sharey=False)
    
    # 设置字体大小
    label_fontsize = 20
    ticks_fontsize = 18
    legend_fontsize = 18
    
    # 帮助函数：添加子图标签
    def add_label(ax, label):
        ax.text(0.5, -0.35, label, transform=ax.transAxes, fontsize=label_fontsize,
                fontweight='bold', va='top', ha='center')

    # 设置公共 y 轴刻度和标签的间隔显示
    y_ticks_scores = np.linspace(0, 10, 5)
    y_ticks_relational = np.linspace(-1, 1, 5)

    # 四个子图共享的代码段
    for ax in axs:
        ax.set_xlabel('Rounds', fontsize=label_fontsize)
        ax.set_xticks(x)
        ax.set_xticklabels([str(i) for i in range(len(conflict_score))], fontsize=ticks_fontsize)
        ax.grid(True)
        ax.tick_params(axis='y', labelsize=ticks_fontsize)

    # 第一个子图
    axs[0].plot(x, conflict_score, color=cm_r(0.8), marker='o', label='Conflict level')
    axs[0].plot(x, emotional_intensity, color=cm_r(0.4), marker='s', label='Emotional intensity')
    axs[0].set_ylabel('Scores', fontsize=label_fontsize)
    axs[0].set_yticks(y_ticks_scores)
    axs[0].set_ylim(0, 10)
    axs[0].legend(loc='best', fontsize=legend_fontsize)
    add_label(axs[0], '(a) Interaction Evaluation')

    # 第二个子图
    axs[1].plot(x, satisfaction, color=cm(0.8), marker='^', label='Satisfaction level')
    axs[1].plot(x, emotional_pressure, color=cm(0.4), marker='D', label='Emotional pressure')
    axs[1].set_ylabel('Scores', fontsize=label_fontsize)
    axs[1].set_yticks(y_ticks_scores)
    axs[1].set_ylim(0, 10)
    axs[1].legend(loc='best', fontsize=legend_fontsize)
    add_label(axs[1], '(b) Agent Interview')

    # 第三个子图
    axs[2].plot(x, social_network, color=cm_g(0.4), marker='x', label='Social network relationship')
    axs[2].set_ylabel('Edge Weights', fontsize=label_fontsize)
    axs[2].set_yticks(y_ticks_relational)
    axs[2].set_ylim(-1, 1)
    axs[2].legend(loc='lower right', fontsize=legend_fontsize)

    # 第四个子图
    axs[3].plot(x, cooperate_num, color=cm_g(0.6), marker='P', label='Cooperation')
    axs[3].plot(x, conflict_num, color=cm_g(0.2), marker='v', label='Conflict')
    axs[3].set_ylabel('Num of Relations', fontsize=label_fontsize)

    max_y4 = max(max(cooperate_num), max(conflict_num))
    max_y4_rounded = ((max_y4 // 1000) + 1) * 1000  # 向上取整到最接近的50

    axs[3].set_yticks(np.linspace(0, max_y4_rounded, 5))  # 使用5个较大的刻度标记
    axs[3].set_ylim(0, max_y4_rounded)
    axs[3].legend(loc='center right', fontsize=legend_fontsize)

    # 添加 (c) 标签在第三和第四个子图中间
    fig.text(0.75, 0.12, '(c) Social Network Analysis', ha='center', fontsize=label_fontsize, fontweight='bold')

    # 调整子图和标签的布局
    plt.tight_layout()
    plt.subplots_adjust(wspace=0.3)  # 调整子图之间的水平间距
    plt.savefig('/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/pic/research_metrics_en.png', bbox_inches='tight')
    plt.show()

def draw_individual_plots(conflict_score, emotional_intensity, satisfaction, emotional_pressure, social_network, cooperate_num, conflict_num):
    plt.rcParams['font.family'] = 'Times New Roman'
    # 横坐标
    x = np.arange(len(conflict_score))
    # 使用 colormap 生成配色方案
    cm_r = plt.get_cmap('coolwarm')  
    cm = plt.get_cmap('cividis')     
    cm_g = plt.get_cmap('viridis')   
    # 设置字体大小
    label_fontsize = 20
    ticks_fontsize = 18
    legend_fontsize = 18
    title_fontsize = 22

    # 第一个子图
    plt.figure(figsize=(6, 4))
    plt.plot(x, conflict_score, color=cm_r(0.7), marker='o', label='Conflict level')
    plt.plot(x, emotional_intensity, color=cm_r(0.2), marker='s', label='Emotional intensity')
    plt.xlabel('Rounds', fontsize=label_fontsize)
    plt.ylabel('Scores', fontsize=label_fontsize)
    plt.xticks(x, [str(i) for i in range(len(conflict_score))], fontsize=ticks_fontsize)
    plt.yticks(np.arange(0, 11, 2))
    plt.ylim(0, 10)
    plt.legend(loc='best', fontsize=legend_fontsize)
    plt.grid(True)
    plt.tick_params(axis='y', labelsize=ticks_fontsize)
    plt.tight_layout()
    plt.savefig('/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/pic/interaction_evaluation.png', bbox_inches='tight')
    plt.close()

    # 第二个子图
    plt.figure(figsize=(6, 4))
    plt.plot(x, satisfaction, color=cm(0.8), marker='^', label='Satisfaction level')
    plt.plot(x, emotional_pressure, color=cm(0.3), marker='D', label='Emotional pressure')
    plt.xlabel('Rounds', fontsize=label_fontsize)
    plt.ylabel('Scores', fontsize=label_fontsize)
    plt.xticks(x, [str(i) for i in range(len(conflict_score))], fontsize=ticks_fontsize)
    plt.ylim(0, 10)
    plt.legend(loc='best', fontsize=legend_fontsize)
    plt.grid(True)
    plt.tick_params(axis='y', labelsize=ticks_fontsize)
    plt.tight_layout()
    plt.savefig('/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/pic/agent_interview.png', bbox_inches='tight')
    plt.close()

    # 第三个子图（Social network relationship）
    plt.figure(figsize=(6, 4))
    plt.plot(x, social_network, color=cm_g(0.8), marker='x', label='Social network relationship')
    plt.xlabel('Rounds', fontsize=label_fontsize)
    plt.ylabel('Relation Value', fontsize=label_fontsize)
    plt.xticks(x, [str(i) for i in range(len(conflict_score))], fontsize=ticks_fontsize)
    plt.ylim(-1, 1)
    plt.legend(loc='best', fontsize=legend_fontsize)
    plt.grid(True)
    plt.tick_params(axis='y', labelsize=ticks_fontsize)
    plt.tight_layout()
    plt.savefig('/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/pic/social_network_relationship.png', bbox_inches='tight')
    plt.close()

    # 第四个子图（Cooperation and Conflict relations）
    plt.figure(figsize=(6, 4))
    plt.plot(x, cooperate_num, color=cm_g(0.5), marker='P', label='Cooperation relations')
    plt.plot(x, conflict_num, color=cm_g(0.2), marker='v', label='Conflict relations')
    plt.xlabel('Rounds', fontsize=label_fontsize)
    plt.ylabel('Num of Relations', fontsize=label_fontsize)
    plt.xticks(x, [str(i) for i in range(len(conflict_score))], fontsize=ticks_fontsize)
    plt.legend(loc='best', fontsize=legend_fontsize)
    plt.grid(True)
    plt.tick_params(axis='y', labelsize=ticks_fontsize)
    plt.tight_layout()
    plt.savefig('/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/pic/social_network_relations.png', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    round_paths=[500,1000, 2000]
    round = 6
    # 初始化数据结构
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
    # 收集所有轮次数据
    filename = f'{round}/user_assessment.json'     
    data = {}   
    i = 0
    for round_path in round_paths:
        with open(os.path.join(f'/home/share/xutianjiao/code/social_simulation/norm_mediator/MEDIATOR/data/{round_path}', filename), 'r') as f:
            data0 = json.load(f)
            for j in data0.values():
                data[i] = j
                i += 1
        # 假设JSON结构为{round_num: data}，如{"1": {}, "2": {}}
    for round_data in data.values():
        for round_num in range(round):
            process_single_round(round_num, round_data, metrics)

    # 排序轮次并生成报告
    sorted_rounds = sorted(metrics['conflict_score'].keys(), key=int)
    analysis_report =  generate_report(metrics, sorted_rounds)
    
        
    # 输出示例（可根据需要格式化为JSON或表格）
    print("=== 交互分析 ===")
    print("1. 冲突分数")
    conflict_score = [float(f"{value['avg']:.2f}") for value in analysis_report['conflict_score']]
    print(conflict_score)
    print("2. 情绪激烈程度")
    emotional_intensity = [float(f"{value['avg']:.2f}") for value in analysis_report['emotional_intensity']]
    print(emotional_intensity)
    
    print("=== 用户采访 ===")
    print("1. 满意度")
    satisfaction = [float(f"{value['avg']:.2f}") for value in analysis_report['satisfaction']]
    print(satisfaction)
    print("2. 情绪压力")
    emotional_pressure = [float(f"{value['avg']:.2f}") for value in analysis_report['emotional_pressure']]
    print(emotional_pressure)
    
    print("\n=== 社交网络权重分析 ===")
    social_network = [float(f"{value:.2f}") for value in analysis_report['social_network'].values()]
    print(social_network)
    cooperate_num = [int(value) for value in analysis_report['cooperate_num'].values()]
    print(cooperate_num)
    conflict_num = [int(value) for value in analysis_report['conflict_num'].values()]
    print(conflict_num)
    draw_pic(conflict_score, emotional_intensity, satisfaction, emotional_pressure, social_network, cooperate_num, conflict_num)
    # draw_individual_plots(conflict_score, emotional_intensity, satisfaction, emotional_pressure, social_network, cooperate_num, conflict_num)