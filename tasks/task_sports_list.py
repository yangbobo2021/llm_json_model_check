

TASK_PROMPT = """
Give me a JSON dict with names of famous athletes & their sports.
Output should format as:
```json
{
    "athletes": [
        {
            "name": "<user name>",
            "sport": "<sport name>"
        }
    ]
}
```
"""

def task_messages():
    return [
        {"role": "user", "content": TASK_PROMPT}
    ]

def check_task_result(result):
    if not "athletes" in result or len(result) != 1:
        print("-- athletes not in result")
        return False
    if not isinstance(result["athletes"], list):
        print("-- athletes not a list")
        return False
    for athlete in result["athletes"]:
        if not "name" in athlete or not "sport" in athlete or len(athlete)!= 2:
            print("-- athlete not valid")
            return False
    return True
