from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict
from course_manager.helpers import date_helper
from course_manager.models.project_settings import ProjectSettings


@dataclass
class ScheduleProject:
    project_id: str
    name: str
    course_code: str
    due_time: Optional[str] = None


class Schedule:
    """Represents a schedule containing projects.

    === Private attributes ===
    _schedule: dictionary matching date to a list of unsorted projects on that date
    _unscheduled: a list of unscheduled projects
    """
    _schedule: Dict[str, List[ScheduleProject]]
    _unscheduled: List[ScheduleProject]

    def __init__(self):
        self._schedule = {}
        self._unscheduled = []

    def add_project(self, course_code: str, project_settings: ProjectSettings):
        """Add project into schedule."""
        if project_settings.due_date is None:
            # No due date, add to unscheduled
            self._unscheduled.append(ScheduleProject(project_settings.project_id,
                                                     project_settings.name, course_code, None))
        else:
            # Get date and time string
            date = date_helper.str_from_date(project_settings.due_date,
                                             date_helper.DATE_FORMAT_DATE)
            time = date_helper.str_from_date(project_settings.due_date,
                                             date_helper.DATE_FORMAT_TIME)

            # Create new list if needed
            if date not in self._schedule:
                self._schedule[date] = []

            # Add project to schedule at the date
            self._schedule[date].append(ScheduleProject(project_settings.project_id,
                                                        project_settings.name, course_code, time))

    def get_schedule(self) -> Tuple[List[Tuple[str, List[ScheduleProject]]],
                                    List[ScheduleProject]]:
        """Get a tuple containing (scheduled, unscheduled) where:

        scheduled: a sorted list of tuples containing (date, projects) where projects
        are all the projects on the day date, sorted from earliest to latest.

        unscheduled: a list of unscheduled projects
        """
        sorted_schedule = []

        for date in self._schedule:
            # Sort each date's schedule by time
            sorted_projects = sorted(self._schedule[date], key=lambda p: p.due_time or '00:00')
            sorted_schedule.append((date, sorted_projects))

        # Sort by date
        sorted_schedule.sort()

        return sorted_schedule, self._unscheduled
