from __future__ import annotations
import json
from dataclasses import dataclass
from typing import Dict, Optional, Any
from course_manager.helpers import date_helper


@dataclass
class TodoItem:
    title: str
    description: str = ''
    is_complete: bool = False
    due_date: Optional[date_helper.datetime] = None
    priority: int = 0

    @staticmethod
    def from_json(obj: Dict[str, Any]) -> Optional[TodoItem]:
        """Parse an json object into TodoItem.

        Return None if the object is invalid.
        """
        try:
            due_date = date_helper.date_from_str(obj['due_date']) if 'due_date' in obj else None
            return TodoItem(obj['title'], obj['description'], obj['is_complete'], due_date, obj['priority'])
        except (json.decoder.JSONDecodeError, KeyError):
            return None

    def to_json(self) -> Dict[str, Any]:
        """Return the JSON representation of TodoItem."""
        obj = {
            'title': self.title,
            'description': self.description,
            'is_complete': self.is_complete,
            'priority': self.priority,
        }

        if self.due_date is not None:
            obj['due_date'] = date_helper.str_from_date(self.due_date)

        return obj
