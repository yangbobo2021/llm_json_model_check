

TASK_PROMPT = """
Add docstring for my function:
```python
def parse_json(content):
    json_block = locate_json_block(content)

    try:
        return json.loads(json_block, strict=False)
    except Exception:
        pass

    json_block = fix_json_error(json_block)
    return json.loads(json_block, strict=False)
```

You just output the new code with JSON format, it should looks like:
```json
{
    "new_code": "<new code>"
}
```
"""

def task_messages():
    return [
        {"role": "user", "content": TASK_PROMPT}
    ]

def check_task_result(result):
    if not "new_code" in result or len(result) != 1:
        return False
    return True
