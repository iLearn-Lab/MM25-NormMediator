#!/bin/bash

data_size=500  # 变量赋值时不加 "$"
round=0

# 初始化阶段
init_scripts=(
    "01_initialize_situation_agent.py"
    "02_1_initialize_social_norm.py"
    "02_2_initialize_personal_norm.py"
    "03_generate_dialogue.py"
)

for script in "${init_scripts[@]}"; do
    python "$script" --data_size "$data_size" --round "$round"
done

# python filter_data.py --data_size "$data_size" --round "$round"

# 主要循环处理

# python 04_1_summary_update_properties.py  --data_size $data_size --round 1
# python 04_2_summarize_dialogue_norms.py  --data_size $data_size --round 1
# python 05_1_interaction_evaluation.py  --data_size $data_size --round 1
# python 05_2_user_assessment.py  --data_size $data_size --round 1
# python 06_1_norm_mediation.py  --data_size $data_size --round 1
# python 06_2_mediation_interaction.py  --data_size $data_size --round 1
# python filter_data.py --data_size $data_size --round 1

# python 04_1_summary_update_properties.py  --data_size $data_size --round 2
# python 04_2_summarize_dialogue_norms.py  --data_size $data_size --round 2
# python 05_1_interaction_evaluation.py  --data_size $data_size --round 2
# python 05_2_user_assessment.py  --data_size $data_size --round 2
# python 06_1_norm_mediation.py  --data_size $data_size --round 2
# python 06_2_mediation_interaction.py  --data_size $data_size --round 2
# python filter_data.py --data_size $data_size --round 2

# python 04_1_summary_update_properties.py  --data_size $data_size --round 3
# python 04_2_summarize_dialogue_norms.py  --data_size $data_size --round 3
# python 05_1_interaction_evaluation.py  --data_size $data_size --round 3
# python 05_2_user_assessment.py  --data_size $data_size --round 3
# python 06_1_norm_mediation.py  --data_size $data_size --round 3
# python 06_2_mediation_interaction.py  --data_size $data_size --round 3
# python filter_data.py --data_size $data_size --round 3

# python 04_1_summary_update_properties.py  --data_size $data_size --round 4
# python 04_2_summarize_dialogue_norms.py  --data_size $data_size --round 4
# python 05_1_interaction_evaluation.py  --data_size $data_size --round 4
# python 05_2_user_assessment.py  --data_size $data_size --round 4
# python 06_1_norm_mediation.py  --data_size $data_size --round 4
# python 06_2_mediation_interaction.py  --data_size $data_size --round 4
# python filter_data.py --data_size $data_size --round 4

# python 04_1_summary_update_properties.py  --data_size $data_size --round 5
# python 04_2_summarize_dialogue_norms.py  --data_size $data_size --round 5
# python 05_1_interaction_evaluation.py  --data_size $data_size --round 5
# python 05_2_user_assessment.py  --data_size $data_size --round 5
# python 06_1_norm_mediation.py  --data_size $data_size --round 5
# python 06_2_mediation_interaction.py  --data_size $data_size --round 5
# python filter_data.py --data_size $data_size --round 5

# python 04_1_summary_update_properties.py  --data_size $data_size --round 6
# python 04_2_summarize_dialogue_norms.py  --data_size $data_size --round 6
# python 05_1_interaction_evaluation.py  --data_size $data_size --round 6
# python 05_2_user_assessment.py  --data_size $data_size --round 6
# python filter_data.py --data_size $data_size --round 6

for round in $(seq 1 6); do
    main_scripts=(
        "04_1_summary_update_properties.py"
        "04_2_summarize_dialogue_norms.py"
        "05_1_interaction_evaluation.py"
        "05_2_user_assessment.py"
    )

    for script in "${main_scripts[@]}"; do
        python "$script" --data_size "$data_size" --round "$round"
    done

    if [ "$round" -le 5 ]; then
        mediation_scripts=(
            "06_1_norm_mediation.py"
            "06_2_mediation_interaction.py"
        )

        for script in "${mediation_scripts[@]}"; do
            python "$script" --data_size "$data_size" --round "$round"
        done
    fi

    # python filter_data.py --data_size "$data_size" --round "$round"
done

# CUDA_VISIBLE_DEVICES=0,7 vllm serve /home/share/xutianjiao/code/pretrained/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B    --port 8882  --tensor-parallel-size 2 --max-model-len 40000 --enforce-eager --gpu_memory_utilization=0.98 --enable-chunked-prefill  --served-model-name llama3
