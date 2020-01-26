import re
import shutil
from typing import List, Optional
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


def get_course_codes() -> List[str]:
    """Get the list of course codes of existing courses, sorted alphabetically.
    """
    return _get_course_codes(paths.get_base_path())


def get_archived_course_codes() -> List[str]:
    """Get the list of course codes of archived courses, sorted alphabetically.
    """
    return _get_course_codes(paths.get_path(ARCHIVED_DIRECTORY))


def get_all_course_codes() -> List[str]:
    """Get the sorted list of course codes of all courses, both archive and current.
    """
    lst = get_course_codes() + get_archived_course_codes()
    lst.sort()
    return lst


def _get_course_codes(directory: paths.Path) -> List[str]:
    """Utility function to get the list containing all course codes in <directory>.

    The returned list is sorted alphabetically.
    """
    # Check if the given path is a directory
    if not directory.is_dir():
        return []

    def get_code(path: paths.Path) -> Optional[str]:
        """Get the course code for the directory <path>.

        Return None if it is not a valid course code, or if path is not a directory.
        """
        if path.is_dir():
            code = path.name
            if code != ARCHIVED_DIRECTORY and is_valid(code):
                return code

    lst = [code for path in directory.iterdir() if (code := get_code(path)) is not None]
    lst.sort()
    return lst
