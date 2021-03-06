import re
import shutil
from typing import Optional, List
from course_manager.models.project_settings import ProjectSettings
from course_manager.helpers import path_helper
from course_manager.constants import MAX_PROJECT_ID_CHARS, MAX_PROJECT_NAME_CHARS

PROJECT_SETTINGS_FILE = '.cm_project_settings'


def project_id_is_valid(project_id: str) -> bool:
    """Return True iff the <project_id> is a valid project id.

    A valid project id:
    - has length between 1 and MAX_PROJECT_ID_CHARS
    - contains only letters, digits, and underscores
    """
    return (re.match(r'^\w+$', project_id) is not None
            and len(project_id) <= MAX_PROJECT_ID_CHARS)


def project_name_is_valid(project_name: str) -> bool:
    """Return True iff the <project_name> has length between 1 and MAX_PROJECT_NAME_CHARS."""
    return 1 <= len(project_name) <= MAX_PROJECT_NAME_CHARS


def project_exists(course_code: str, project_id: str) -> bool:
    """Check whether the project with <project_id> exist in course with <course_code>."""
    return path_helper.get_path(course_code, project_id).is_dir()


def get_project_ids(course_code: str) -> List[str]:
    """Return the list of ids of the course's projects.

    Precondition: the course with <course_code> exists.
    """
    project_ids = []

    for path in path_helper.get_path(course_code).iterdir():
        if path.is_dir():
            project_ids.append(path.name)

    return project_ids


def create_project(course_code: str, settings: ProjectSettings):
    """Create a new project with given course code and settings.

    Preconditions:
    - the course with <course_code> exists
    - the project id is valid and unique from other projects of the same course
    """
    project_dir = path_helper.get_path(course_code, settings.project_id)
    project_dir.mkdir(parents=True)

    write_project_settings(course_code, settings)
    # TODO: other initializations, according to template?


def delete_project(course_code: str, project_id: str):
    """Delete the project with given course code and project id.

    Preconditions:
    - the course with <course_code> exists
    - the project with <project_id> exists in the course
    """
    shutil.rmtree(path_helper.get_path(course_code, project_id))


def write_project_settings(course_code: str, settings: ProjectSettings):
    """Write project settings to file.

    Preconditions:
    - the course with <course_code> exists
    - the project directory exists
    """
    settings_path = path_helper.get_path(course_code, settings.project_id, PROJECT_SETTINGS_FILE)

    with open(str(settings_path), 'w') as f:
        f.write(settings.to_json())


def read_project_settings(course_code: str, project_id: str) -> Optional[ProjectSettings]:
    """Read project settings of project with id.

    Return None if the settings file does not exist, or if the content cannot be parsed.

    Preconditions:
    - the course with <course_code> exists
    - the project directory exists
    """
    settings_path = path_helper.get_path(course_code, project_id, PROJECT_SETTINGS_FILE)

    try:
        with open(str(settings_path), 'r') as f:
            content = f.read()
            return ProjectSettings.from_json(content)

    except FileNotFoundError:
        return None
