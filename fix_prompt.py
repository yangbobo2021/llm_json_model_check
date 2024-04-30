

def fix_prompt_for_json(messages):
    system_prompt = "You are a helpful assistant. You must answer the user's question as valid JSON object within '``` json` and '```', don't say anything else."
    # find last message with role as user
    last_user_index = 0
    for index, message in enumerate(messages):
        if message["role"] == "user":
            last_user_index = index
            break
    messages[last_user_index]["content"] = system_prompt + "\n\n" + messages[last_user_index]["content"]
    return messages
