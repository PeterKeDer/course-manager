import click
from typing import Optional
from course_manager.cli import get_params, args, repeat_prompt, date_validator
from course_manager.helpers import todo_helper
from course_manager.models.todo_item import TodoItem
from course_manager.commands.common import check_course_exists, check_project_exists


@click.group('todo')
def cmd_todo():
    """Add, manage, or remove todo items."""


@cmd_todo.command('add')
@get_params(args.COURSE_CODE_OPTIONAL, args.PROJECT_ID_OPTIONAL)
def cmd_todo_add(course_code: Optional[str], project_id: Optional[str]):
    """Add a todo. Todo items can be added to all courses, a course, or a project.
    User will be prompted with options.
    """
    scope = _get_todo_scope(course_code, project_id)

    title = click.prompt('Title', type=str)
    description = click.prompt('Description', default='', type=str)
    due_date = repeat_prompt('Due date', date_validator)
    priority = int(click.prompt('Priority', default='0', type=int))

    item = TodoItem(title, description, False, due_date, priority)

    todo_helper.add_todo_item(item, scope)


@cmd_todo.command('mark')
def cmd_todo_mark():
    """Mark a todo item as complete or incomplete."""


@cmd_todo.command('remove')
def cmd_todo_remove():
    """Remove a todo item."""


def _get_todo_scope(course_code: Optional[str], project_id: Optional[str]) -> todo_helper.TodoScope:
    """Get the TodoScope given <course_code> and <project_id>.

    If any of the two are invalid, display a message and exit with status code 1.
    """
    scope = None

    if course_code is not None:
        check_course_exists(course_code)
        scope = course_code

        if project_id is not None:
            check_project_exists(course_code, project_id)
            scope = (course_code, project_id)

    return scope
