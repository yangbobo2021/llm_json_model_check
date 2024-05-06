

TASK_PROMPT = """
Check for unreasonable variable or function names defined in the code and optimize these names.
Here is my code:
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

You just output as JSON format, it should looks like:
```json
{
    "renames": [
        {"<old name>": "<new name>"}
    ]
}
```
"""

def task_messages():
    return [
        {"role": "user", "content": TASK_PROMPT}
    ]

def check_task_result(result):
    if not "renames" in result or len(result) != 1:
        return False
    if not isinstance(result["renames"], list):
        return False
    return True
