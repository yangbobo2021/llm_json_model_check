import sys
import os
import openai

# append current path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from json_parser import parse_json
from models import model_list
from fix_prompt import fix_prompt_for_json
from tasks import json_tasks, json_task_checkers


def evaluate(api_key, api_base, model_engine):
    check_result = [False]*len(json_tasks)
    for index,task in enumerate(json_tasks):
        messages = task()
        messages = fix_prompt_for_json(messages)

        client = openai.OpenAI(
            api_key = api_key,
            base_url = api_base
        )

        response = client.chat.completions.create(**{
            "model": model_engine,
            "messages": messages,
            "stream": True
        })

        result = ""
        for chunk in response:
            result += chunk.choices[0].delta.content
        
        try:
            print("result:", result)
            result_obj = parse_json(result)
            success = json_task_checkers[index](result_obj)
            check_result[index] = success
        except Exception as e:
            print("parse_json error:", e)
            pass

    return check_result


# 使用argparser设置命令行参数
# -key: OpenAI API key
# -base: OpenAI API base url
# -model: model engine
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-key", "--api_key", required=True, type=str, help="OpenAI API key")
    parser.add_argument("-base", "--base_url", required=True,  type=str, help="OpenAI API base url")
    parser.add_argument("-model", "--model_engine", type=str, help="model engine")
    args = parser.parse_args()

    api_key = args.api_key
    base_url = args.base_url
    model_engine = args.model_engine

    print("model:", model_engine)
    if model_engine and model_engine != "all":
        check_reulst = evaluate(api_key, base_url, model_engine)
        print(check_reulst)
    else:
        model_check_result = {}
        for model_engine in model_list:
            check_reulst = evaluate(api_key, base_url, model_engine)
            model_check_result[model_engine] = check_reulst

        for model in model_check_result:
            print(model, model_check_result[model])
