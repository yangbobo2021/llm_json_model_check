from .task_commit_message import task_messages as task_messages_commit_message, check_task_result as check_task_result_commit_message
from .task_function_rename import task_messages as task_messages_function_rename, check_task_result as check_task_result_function_rename
from .task_sports_list import task_messages as task_messages_sports, check_task_result as check_task_sports
from .task_add_docstring import task_messages as task_messages_docstring, check_task_result as check_task_docstring
from.task_renames import task_messages as task_messages_renames, check_task_result as check_task_renames

json_tasks = [
    task_messages_commit_message,
    task_messages_function_rename,
    task_messages_sports,
    task_messages_docstring,
    task_messages_renames
]

json_task_checkers = [
    check_task_result_commit_message,
    check_task_result_function_rename,
    check_task_sports,
    check_task_docstring,
    check_task_renames
]
