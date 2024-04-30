import json


def parse_json(content):
    content = content.strip()
    if content.startswith("```"):
        content = content[3:]
    elif content.find("```") > 0:
        content = content[content.find("```") + 3:]
    content = content.strip()
    if content.startswith("json"):
        content = content[4:]
    content = content.strip()
    if content.endswith("```"):
        content = content[:-3]
    elif content.find("```") > 0:
        content = content[:content.find("```")]
    content = content.strip()
    content = content.replace("\\_", "_")

    try:
        return json.loads(content)
    except Exception:
        lines = content.split("\n")
        for line_index, line in enumerate(lines):
            line = line.strip()
            if not line.endswith("\""):
                continue

            index_split = line.find(":")
            if index_split > 0:
                value_start = line.find("\"", index_split+1)
                if value_start > 0:
                    value_end = line.rfind("\"")
                    if value_end > 0:
                        value = line[value_start+1:value_end]
                        value_new = value.replace("\"", "\\\"")
                        print(value_new)
                        lines[line_index] = line[:value_start+1] + value_new + line[value_end:]
        content = "\n".join(lines)
    return json.loads(content)
