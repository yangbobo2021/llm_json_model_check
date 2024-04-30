

TASK_PROMPT = """
Here is my new function:
``` python
def print_hello():
    print("hello")
```
base my chanages, generate a commit message, format as {"title": "<title>", "body": "<body>"}
"""

def task_messages():
    return [
        {"role": "user", "content": TASK_PROMPT}
    ]

def check_task_result(result):
    if "title" in result and "body" in result and len(result) == 2:
        return True
    return False
