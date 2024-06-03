
在GIT ACTION中对新模型进行验证，确定当前模型在不同任务上JSON的支持程度。

## 前置依赖
1. 通过BENCH_REPORT宏设定了benchmark的结果报告所在目录；
2. 通过OPENAI_API_KEY设定了LLM模型服务的KEY；
3. 通过OPENAI_API_BASE设定了LLM模型服务的BASE URL。

## 执行脚本命令
conda create -n json_benchmark python=3.11
conda activate json_benchmark
pip install -r .
python ./benchmark.py --model xx --threads 10
