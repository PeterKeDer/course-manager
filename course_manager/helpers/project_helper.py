import re
import shutil
from typing import Optional
from course_manager.models.project_settings import ProjectSettings
from course_manager.helpers import path_helper

PROJECT_SETTINGS_FILE = '.cm_project_settings'


def project_id_is_valid(project_id: str) -> bool:
    """Return True iff the <project_id> is a valid project id.

    A valid project id:
    - has length of at least 1
    - contains only letters, digits, and underscores
    """
    return re.match(r'^\w+$', project_id) is not None


def project_exists(course_code: str, project_id: str) -> bool:
    """Check whether the project with <project_id> exist in course with <course_code>.
    """
    return path_helper.get_path(course_code, project_id).is_dir()


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
