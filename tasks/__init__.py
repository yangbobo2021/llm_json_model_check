from .task_commit_message import task_messages as task_messages_commit_message, check_task_result as check_task_result_commit_message
from .task_function_rename import task_messages as task_messages_function_rename, check_task_result as check_task_result_function_rename

json_tasks = [
    task_messages_commit_message,
    task_messages_function_rename,
]

json_task_checkers = [
    check_task_result_commit_message,
    check_task_result_function_rename,
]
