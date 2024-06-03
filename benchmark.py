import datetime
import json
import sys
import os
import time
import openai
import concurrent.futures
import importlib.util

# append current path to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# from models import model_list
# from tasks import json_tasks, json_task_checkers


def evaluate_task(api_key, api_base, model_engine, task, result_dir):
    start_time = time.time()

    result_task_dir = os.path.join(result_dir, task)
    os.makedirs(result_task_dir, exist_ok=True)
    result_task_log = os.path.join(result_task_dir, "log.txt")
    result_task_report = os.path.join(result_task_dir, ".devchat.results.json")

    task_dir = os.path.join("tasks", task)
    task_py = os.path.join(task_dir, "task.py")

    # load task_py
    spec = importlib.util.spec_from_file_location("task", task_py)
    task_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(task_module)

    messages = task_module.task_messages()
    checker = task_module.check_task_result

    def save_report(result, duration):
        nonlocal task
        nonlocal model_engine
        nonlocal result_task_report
        result_data = {
            "testcase": task,
            "model": model_engine,
            "tests_outcomes": [result],
            "duration": duration
        }
        with open(result_task_report, "w+", encoding="utf-8") as file:
            file.write(json.dumps(result_data, indent=4))
            file.write("\n")

    try:
        with open(result_task_log, "w+", encoding="utf-8") as file:
            try:
                client = openai.OpenAI(
                    api_key = api_key,
                    base_url = api_base
                )

                response = client.chat.completions.create(**{
                    "model": model_engine,
                    "messages": messages,
                    "stream": True,
                    "response_format": {"type": "json_object"},
                })

                result = ""
                try:
                    for chunk in response:
                        result += chunk.choices[0].delta.content
                except openai.APIError as error:
                    file.write(f"Exception: {error}")
                    file.write("\n")
                    print("openai error:", error)
                    save_report(False, time.time()-start_time)
                    return False, time.time()-start_time
                except Exception as err:
                    file.write(f"Exception: {err}")
                    file.write("\n")
                    print("exception:", err)
                    save_report(False, time.time()-start_time)
                    return False, time.time()-start_time
                file.write(f"Receive: {result}")
                file.write("\n")

                try:
                    print("result:", result)
                    result_obj = json.loads(result)
                    success = checker(result_obj)
                    save_report(success, time.time()-start_time)
                    return success, time.time()-start_time
                except Exception as e:
                    file.write(f"Exception: {e}")
                    file.write("\n")
                    print("parse_json error:", e)
                    save_report(False, time.time()-start_time)
                    return False, time.time()-start_time
            except Exception as err:
                file.write(f"Exception: {err}")
                file.write("\n")
                print("Exception:", err)
                save_report(False, time.time()-start_time)
                return False, time.time()-start_time
    except Exception:
        save_report(False, time.time()-start_time)
        return False, time.time()-start_time


class CustomFuture(concurrent.futures.Future):
    def __init__(self, task):
        super().__init__()
        self.task_id = task

def evaluate_model(api_key, api_base, model_engine, threads, output):
    """ run benchmark """
    result_dir = "json_benchmark_{}".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    result_dir = os.path.join(output, result_dir)

    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [CustomFuture(subdir) for subdir in os.listdir("tasks") if os.path.isdir(os.path.join("tasks", subdir)) and os.path.isdir(os.path.join("tasks", subdir, ".docs"))]
        for future in futures:
            executor.submit(evaluate_task, api_key, api_base, model_engine, future.task_id, result_dir).add_done_callback(future.set_result)
        results = [(future.task_id, future.result().result()) for future in concurrent.futures.as_completed(futures)]
    return {"model": model_engine, "tasks": results}


# 使用argparser设置命令行参数
# -key: OpenAI API key
# -base: OpenAI API base url
# -model: model engine
import argparse

def main():
    print("---> start json benchmark")
    parser = argparse.ArgumentParser()
    parser.add_argument("-key", "--api_key", required=True, type=str, help="OpenAI API key")
    parser.add_argument("-base", "--base_url", required=True,  type=str, help="OpenAI API base url")
    parser.add_argument("-model", "--model", required=True, type=str, help="model engine")
    parser.add_argument("-threads", "--threads", type=int, help="threads num", default=1)
    parser.add_argument("-output", "--output", required=True, type=str, help="result directory")
    args = parser.parse_args()

    api_key = args.api_key
    base_url = args.base_url
    model_engine = args.model
    threads = args.threads
    output = args.output

    print("model:", model_engine)

    result = evaluate_model(api_key, base_url, model_engine, threads, output)
    print("-------------->>:")
    print(result)

if __name__ == "__main__":
    main()
