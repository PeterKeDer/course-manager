from __future__ import annotations
import json
from typing import Optional
from datetime import datetime
from course_manager.helpers import date_helper

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


class ProjectSettings:
    name: str
    project_id: str
    due_date: Optional[datetime]
    open_method: Optional[str]

    def __init__(self, name: str, project_id: str, due_date: Optional[datetime],
                 open_method: Optional[str]):
        self.name = name
        self.project_id = project_id
        self.due_date = due_date
        self.open_method = open_method

    @staticmethod
    def from_json(json_str: str) -> Optional[ProjectSettings]:
        """Parse a json string into ProjectSettings.

        Return None if the string is invalid.
        """
        try:
            obj = json.loads(json_str)

            try:
                due_date = date_helper.date_from_str(obj['due_date'])
            except KeyError:
                due_date = None

            try:
                open_method = obj['open_method']
            except KeyError:
                open_method = None

            return ProjectSettings(obj['name'], obj['project_id'], due_date, open_method)

        except (json.decoder.JSONDecodeError, KeyError):
            return None

    def to_json(self) -> str:
        """Convert to json string representation."""
        obj = {
            'name': self.name,
            'project_id': self.project_id,
        }

        if self.due_date is not None:
            obj['due_date'] = date_helper.str_from_date(self.due_date)

        if self.open_method is not None:
            obj['open_method'] = self.open_method

        return json.dumps(obj)
