import click
from typing import List, Optional
from course_manager.cli import get_params, args, colors
from course_manager.helpers import course_helper, schedule_helper
from course_manager.models.schedule import ScheduleProject
from course_manager import constants

PROJECT_PREFIX = '  '


@click.command('schedule')
@get_params(args.COURSE_CODES)
def cmd_schedule(course_codes: List[str]):
    """Show due dates of projects in order.

    If course_codes are given, show due dates for only those courses.
    """
    if len(course_codes) == 0:
        # Show all courses
        courses = course_helper.get_course_codes()
    else:
        # Show only some courses
        courses = [course for course in course_codes
                   if course_helper.course_code_is_valid(course)
                   and course_helper.course_exists(course)]

    # Get schedule using courses
    schedule = schedule_helper.get_schedule(courses)
    scheduled, unscheduled = schedule.get_schedule()

    # TODO: consider adding color in separate course settings

    # Get a random color for each course
    course_colors = colors.get_colors(len(courses))
    course_to_color = {}
    for i in range(len(courses)):
        course_to_color[courses[i]] = course_colors[i]

    # Display header
    click.secho(PROJECT_PREFIX +
                'Date/Time'.ljust(constants.MAX_DUE_TIME_CHARS + 1) +
                'Course'.ljust(constants.MAX_COURSE_CODE_CHARS + 2 + 1) +
                'Name'.ljust(constants.MAX_PROJECT_NAME_CHARS + 1) +
                'Project Id'.ljust(constants.MAX_PROJECT_ID_CHARS + 2) + '\n',
                bold=True)

    # Display scheduled projects
    for date, projects in scheduled:
        click.secho(date, bold=True)

        for project in projects:
            click.echo(_get_project_str(project, course_to_color[project.course_code],
                                        prefix=PROJECT_PREFIX))

    # Display unscheduled projects
    if len(unscheduled) == 0:
        click.secho('No unscheduled projects.', bold=True)
    else:
        click.secho('Unscheduled', bold=True)
        for project in unscheduled:
            click.echo(_get_project_str(project, course_to_color[project.course_code],
                                        prefix=PROJECT_PREFIX))


def _get_project_str(project: ScheduleProject, course_color: Optional[str] = None,
                     prefix: str = '') -> str:
    """Get the styled string for a project, with an optional prefix."""
    course = click.style(f'[{project.course_code}]'.ljust(constants.MAX_COURSE_CODE_CHARS + 2),
                         bold=True, fg=course_color)
    project_id = f'({project.project_id})'.ljust(constants.MAX_PROJECT_ID_CHARS + 2)
    project_name = project.name.ljust(constants.MAX_PROJECT_NAME_CHARS)

    # Hide times at 00:00 or those that don't exist
    if project.due_time == '00:00' or project.due_time is None:
        due_time = ''
    else:
        due_time = project.due_time
    due_time = due_time.ljust(constants.MAX_DUE_TIME_CHARS + 1)

    return f'{prefix}{due_time}{course} {project_name} {project_id}'
