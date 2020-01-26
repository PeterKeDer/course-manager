import re
import shutil
import course_manager.helpers.path_helper as paths

ARCHIVED_DIRECTORY = '.course_manager_archived'


def is_valid(course_code: str) -> bool:
    """Return True iff <course_code> is a valid course code.

    A valid course code:
        - has length of at least 1
        - contains only letters, digits, and underscores
        - is lowercase
    """
    return re.match(r'^[a-z0-9_]+$', course_code) is not None


def add_course(course_code: str):
    """Add a new course with code <course_code>.

    Preconditions:
        - the course code is valid
        - the course does not already exist or in archive
    """
    paths.get_path(course_code).mkdir(parents=True)
    # TODO: other initializations


def remove_course(course_code: str):
    """Remove the course with code <course_code>

    Preconditions:
        - the course code is valid
        - the course exists
    """
    shutil.rmtree(paths.get_path(course_code))


def archive_course(course_code: str):
    """Move the course with code <course_code> from archived to courses.

    Preconditions:
        - the course code is valid
        - the course exists
    """
    src = paths.get_path(course_code)
    dest = paths.get_path(ARCHIVED_DIRECTORY, course_code)
    shutil.move(str(src), str(dest))


def unarchive_course(course_code: str):
    """Move the course with code <course_code> from archived to courses.

    Preconditions:
        - the course code is valid
        - the course exists in archive
    """
    src = paths.get_path(ARCHIVED_DIRECTORY, course_code)
    dest = paths.get_path(course_code)
    shutil.move(str(src), str(dest))


def course_exists(course_code: str) -> bool:
    """Return True iff the course with <course_code> exists.

    Precondition: the course code is valid.
    """
    return paths.get_path(course_code).exists()


def course_archived(course_code: str) -> bool:
    """Return True iff the course with <course_code> exists in archive.

    Precondition: the course code is valid.
    """
    return paths.get_path(ARCHIVED_DIRECTORY, course_code).exists()
