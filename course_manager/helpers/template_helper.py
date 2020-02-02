import re
import shutil
from typing import Optional
from course_manager.helpers import path_helper

TEMPLATES_DIRECTORY = 'templates'


def template_name_is_valid(template: str) -> bool:
    """Return True iff the template name is valid.

    A valid template name:
    - has length of at least 1
    - contains only letters, numbers, and underscores
    """
    return re.match(r'^[a-z0-9_]+$', template) is not None


def template_exists(template: str, course_code: Optional[str] = None):
    """Return True iff the template exists.

    If <course_code> is given, check in the course's templates folder instead.

    Preconditions:
    - <template> is a valid template name
    - <course_code> is a valid course code if given
    """
    return get_template_path(template, course_code).is_dir()


def create_template(template: str, course_code: Optional[str] = None):
    """Create a new template.

    If <course_code> is given, create in the course's directory.

    Preconditions:
    - <template> is a valid template name and unique name within the directory
    - the course with code <course_code> exists
    """
    get_template_path(template, course_code).mkdir(parents=True)


def delete_template(template: str, course_code: Optional[str] = None):
    """Delete a template.

    If <course_code> is given, delete from the course's directory.

    Preconditions:
    - template with name <template> exists
    - the course with code <course_code> exists
    """
    shutil.rmtree(get_template_path(template, course_code))


def get_template_path(template: str, course_code: Optional[str] = None) -> path_helper.Path:
    """Get the path to template."""
    if course_code is not None:
        return path_helper.get_path(course_code, TEMPLATES_DIRECTORY, template)
    return path_helper.get_path(TEMPLATES_DIRECTORY, template)
