

TASK_PROMPT = """
Here is my new function:
``` python
def print_hello():
    print("hello")
```
rename the function, generate new function name, format as {"name": "<name>"}
"""

def task_messages():
    return [
        {"role": "user", "content": TASK_PROMPT}
    ]

def check_task_result(result):
    if "name" in result and len(result) == 1:
        return True
    return False
