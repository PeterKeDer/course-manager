from typing import List
from course_manager.helpers import project_helper
from course_manager.models.schedule import Schedule


def get_schedule(course_codes: List[str]) -> Schedule:
    """Get a Schedule object containing projects of courses in <course_codes>.

    Precondition: all courses in <course_code> exists.
    """
    schedule = Schedule()

    # For each course, add all projects into schedule
    for course_code in course_codes:
        for project_id in project_helper.get_project_ids(course_code):
            settings = project_helper.read_project_settings(course_code, project_id)

            if settings is not None:
                schedule.add_project(course_code, settings)

    return schedule
