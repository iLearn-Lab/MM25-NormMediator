import matplotlib.pyplot as plt
import numpy as np

# 假设有六个时间点的数据
conflict_score = [3.15, 2.98, 3.45, 3.00, 2.85, 3.10]
emotional_intensity = [4.25, 3.95, 3.65, 3.75, 4.00, 3.50]
satisfaction = [4.75, 4.62, 4.44, 4.50, 4.65, 4.55]
emotional_pressure = [2.85, 3.12, 2.98, 3.10, 3.25, 3.00]
social_network = [1.15, 1.30, 1.45, 1.50, 1.55, 1.60]
cooperate_num = [5, 7, 6, 8, 9, 7]
conflict_num = [2, 3, 1, 2, 2, 1]

# 横坐标
x = np.arange(6)

# 使用 colormap 生成配色方案
cm_r = plt.get_cmap('Oranges')  # 使用橙色渐变 colormap
cm = plt.get_cmap('Blues')      # 使用蓝色渐变 colormap
cm_g = plt.get_cmap('Greens')   # 使用绿色渐变 colormap

# 创建水平子图
fig, axs = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

# 设置字体大小
label_fontsize = 16
ticks_fontsize = 14
legend_fontsize = 14
title_fontsize = 18

# 第一个子图
axs[0].plot(x, conflict_score, color=cm_r(0.8), marker='o', label='Conflict level')
axs[0].plot(x, emotional_intensity, color=cm_r(0.4), marker='s', label='Emotional intensity')
axs[0].set_title('Interaction evaluation', fontsize=title_fontsize)
axs[0].set_xlabel('Rounds', fontsize=label_fontsize)
axs[0].set_ylabel('Scores', fontsize=label_fontsize)
axs[0].set_xticks(x)
axs[0].set_xticklabels([str(i) for i in range(6)], fontsize=ticks_fontsize)
axs[0].set_yticks(np.arange(0, 11, 2))
axs[0].set_ylim(0, 10)
axs[0].legend(loc='best', fontsize=legend_fontsize)
axs[0].grid(True)
axs[0].tick_params(axis='y', labelsize=ticks_fontsize)  # 增大 y 轴刻度标签

# 第二个子图
axs[1].plot(x, satisfaction, color=cm(0.8), marker='^', label='Satisfaction')
axs[1].plot(x, emotional_pressure, color=cm(0.4), marker='D', label='Emotional pressure')
axs[1].set_title('Agent Interview', fontsize=title_fontsize)
axs[1].set_xlabel('Rounds', fontsize=label_fontsize)
axs[1].set_xticks(x)
axs[1].set_xticklabels([str(i) for i in range(6)], fontsize=ticks_fontsize)
axs[1].set_ylim(0, 10)
axs[1].legend(loc='best', fontsize=legend_fontsize)
axs[1].grid(True)
axs[1].tick_params(axis='y', labelsize=ticks_fontsize)  # 增大 y 轴刻度标签

# 第三个子图，使用双重 y 轴
ax3_left = axs[2]
ax3_right = ax3_left.twinx()

ax3_left.plot(x, social_network, color=cm_g(0.8), marker='x', label='Social network relationship')
ax3_right.plot(x, cooperate_num, color=cm_g(0.6), marker='v', label='Cooperation relations')
ax3_right.plot(x, conflict_num, color=cm_g(0.4), marker='P', label='Conflict relations')

ax3_left.set_title('Social network analysis', fontsize=title_fontsize)
ax3_left.set_xlabel('Rounds', fontsize=label_fontsize)
ax3_left.set_xticks(x)
ax3_left.set_xticklabels([str(i) for i in range(6)], fontsize=ticks_fontsize)
ax3_left.set_ylim(0, 10)
ax3_right.set_ylabel('Num of relation types', fontsize=label_fontsize)
ax3_left.grid(True)
ax3_left.tick_params(axis='y', labelsize=ticks_fontsize)  # 增大右侧 y 轴刻度标签
ax3_right.tick_params(axis='y', labelsize=ticks_fontsize)  # 增大右侧 y 轴刻度标签

# 设置图例
lines_left, labels_left = ax3_left.get_legend_handles_labels()
lines_right, labels_right = ax3_right.get_legend_handles_labels()
ax3_left.legend(lines_left + lines_right, labels_left + labels_right, loc='best', fontsize=legend_fontsize)

# 布局调整
plt.tight_layout()
plt.savefig('research_metrics_en.png', bbox_inches='tight')
plt.show()