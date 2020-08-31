import json
from typing import List, Tuple, Union
from course_manager.models.todo_item import TodoItem
from course_manager.helpers import path_helper

TodoScope = Union[None, str, Tuple[str, str]]
TODO_FILENAME = '.cm_todos.json'


def get_todo_items(scope: TodoScope) -> List[TodoItem]:
    """Get the todo items from <scope>.

    Precondition: <scope> is a valid scope.
    """
    path = _get_file_path(scope)

    try:
        with open(path, 'r') as f:
            content = f.read()
            # Return the list of parsed todo items, where items that cannot be parsed are discarded
            return [item for obj in json.loads(content)
                    if (item := TodoItem.from_json(obj)) is not None]

    except FileNotFoundError:
        return []


def add_todo_item(item: TodoItem, scope: TodoScope):
    """Add a todo item to <scope>.

    Precondition: <scope> is a valid scope.
    """
    path = _get_file_path(scope)

    try:
        with open(path, 'r') as f:
            content = f.read()
            obj = json.loads(content)
    except FileNotFoundError:
        obj = []

    obj.append(item.to_json())
    json_str = json.dumps(obj)

    with open(path, 'w') as f:
        f.write(json_str)


def _get_file_path(scope: TodoScope) -> str:
    """Get the path string to the todo json file given <scope>."""
    if scope is None:
        return str(path_helper.get_path(TODO_FILENAME))
    elif isinstance(scope, str):
        return str(path_helper.get_path(scope, TODO_FILENAME))
    else:
        # TODO: check projects in subdirectories (possible in future)
        course_code, project_id = scope
        return str(path_helper.get_path(course_code, project_id, TODO_FILENAME))
