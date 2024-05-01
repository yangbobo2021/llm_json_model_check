import json
from typing import List


def index_find(value: str, start_pos: int, flag_list: List[str]):
    for flag in flag_list:
        index = value.find(flag, start_pos)
        if index >= 0:
            return index, flag
    return -1, ""


def locate_json_block(content: str):
    index_start, flag = index_find(content, 0, ["```json", "``` json", "```"])
    if index_start < 0:
        return content

    index_end = content.find("```", index_start + len(flag))
    if index_end < 0:
        return content[index_start + len(flag):]
    return content[index_start + len(flag):index_end]

def fix_unnecessary_slash(json_block: str):
    # /_ -> _
    BACKSLASH = {
        '"': '"', '\\': '\\', '/': '/',
        'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t',
    }

    current_pos = 0
    while True:
        index_slash = json_block.find("\\", current_pos)
        if index_slash < 0:
            break
        if json_block[index_slash + 1] not in BACKSLASH:
            json_block = json_block[:index_slash] + json_block[index_slash + 1:]

        current_pos = index_slash + 1
    return json_block


def next_char(value: str, pos: int):
    for i in range(pos, len(value)):
        # whether value[i] is visible character
        if value[i].isprintable() and not value[i].isspace():
            return i, value[i]
    return -1, ""

def before_char(value: str, pos: int):
    for i in range(pos, -1, -1):
        # whether value[i] is visible character
        if value[i].isprintable() and not value[i].isspace():
            return i, value[i]
    return -1, ""

def fix_quotes(json_block: str):
    # "key": "value "a" "b"" -> "key": "value \"a\" \"b\""
    # valid pairs: ","  ":   "}   "]
    current_pos = 0
    while True:
        index_slash = json_block.find("\"", current_pos)
        if index_slash < 0:
            break

        if json_block[index_slash - 1] == "\\":
            current_pos = index_slash + 1
            continue

        next_pos, next_c = next_char(json_block, index_slash + 1)
        if next_pos < 0:
            break
        _1, before_c = before_char(json_block, index_slash - 1)

        if next_c in [",", ":", "}", "]"] or before_c in [",", ":", "{", "["]:
            current_pos = index_slash + 1
            continue
        else:
            json_block = json_block[:index_slash] + "\\" + json_block[index_slash:]
            current_pos = index_slash + 2
    return json_block


def fix_comma(json_block: str):
    current_pos = 0
    while True:
        index_comma = json_block.find(",", current_pos)
        if index_comma < 0:
            break

        next_pos, next_c = next_char(json_block, index_comma + 1)
        if next_pos < 0:
            break
        if next_c in ["}", "]"]:
            # ignore this comma
            json_block = json_block[:index_comma] + json_block[index_comma + 1:]
            current_pos = index_comma + 1
        else:
            current_pos = index_comma + 1
    return json_block

def fix_json_error(content: str):
    block = fix_unnecessary_slash(content)
    block = fix_quotes(block)
    block = fix_comma(block)
    return block

def parse_json(content):
    json_block = locate_json_block(content)

    try:
        return json.loads(json_block, strict=False)
    except Exception:
        pass

    json_block = fix_json_error(json_block)
    return json.loads(json_block, strict=False)
