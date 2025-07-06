from modelscope import snapshot_download
 
model_dir = snapshot_download('deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', cache_dir='/home/share/xutianjiao/code/pretrained/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B', revision='master')