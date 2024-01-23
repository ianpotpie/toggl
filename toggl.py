from datetime import datetime, timedelta, timezone

from dateutil import parser


def utc_to_datetime(utc_timestamp, tz=None):
    if tz is None:
        tz = datetime.now().astimezone().tzinfo

    # Parse the timestamp
    dt = parser.parse(utc_timestamp)

    # If the timestamp is naive (no timezone info), assume it's in UTC
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        dt = dt.replace(tzinfo=tz)

    return dt


class TimeEntry:
    def __init__(self, **kwargs):
        field_to_type = {
            "at": "datetime",
            "billable": "boolean",
            "client_name": "string",
            "description": "string",
            "duration": "timedelta",
            "duronly": "string",
            "id": "integer",
            "project_color": "string",
            "project_id": "integer",
            "project_name": "string",
            "server_deleted_at": "datetime",
            "start": "datetime",
            "stop": "datetime",
            "tag_ids": "list",
            "tags": "list",
            "task_id": "list",
            "user_id": "integer",
            "workspace_id": "integer",
        }

        for field in field_to_type:
            setattr(self, field, None)

        for field, val in kwargs.items():
            if field not in field_to_type:
                continue
            fieldType = field_to_type[field]

            if fieldType == "datetime" and isinstance(val, str):
                setattr(self, field, utc_to_datetime(val))
                continue

            if (
                field == "duration"
                and (isinstance(val, int) or isinstance(val, float))
                and val >= 0
            ):
                setattr(self, field, timedelta(seconds=val))
                continue

            setattr(self, field, val)

    def __str__(self):
        endStr = None
        if self.stop is not None:
            endStr = self.stop.astimezone().strftime("%Y-%m-%d %H:%M")

        myStr = (
            f"Project: {self.project_name} ({self.id})\n"
            f"Description: {self.description}\n"
            f"Tags: {self.tags}\n"
            f"Start: {self.start.astimezone().strftime('%Y-%m-%d %H:%M')}\n"
            f"End: {endStr}"
        )
        return myStr


class Project:
    def __init__(self, **kwargs):
        field_to_type = {
            "active": "boolean",
            "actual_duration": "timedelta",
            "at": "datetime",
            "auto_estimates": "boolean",
            "billable": "boolean",
            "client_id": "integer",
            "color": "string",
            "created_at": "datetime",
            "currency": "string",
            "current_period": "dictionary",
            "end_date": "datetime",
            "estimated_duration": "timedelta",
            "fixed_fee": "float",
            "id": "integer",
            "is_private": "boolean",
            "name": "string",
            "permissions": "string",
            "rate": "float",
            "rate_last_updated": "datetime",
            "recurring": "boolean",
            "recurring_parameters": "list",
            "server_deleted_at": "string",
            "start_date": "date",
            "status": "string",
            "template": "boolean",
            "template_id": "integer",
            "worksapce_id": "integer",
        }

        for field in field_to_type:
            setattr(self, field, None)

        for field, val in kwargs.items():
            if field not in field_to_type:
                continue
            fieldType = field_to_type[field]

            if fieldType == "datetime" and isinstance(val, str):
                setattr(self, field, utc_to_datetime(val))
                continue

            if (
                field in ["actual_duration", "estimated_duration"]
                and (isinstance(val, int) or isinstance(val, float))
                and val >= 0
            ):
                setattr(self, field, timedelta(seconds=val))
                continue

            setattr(self, field, val)

    def __str__(self):
        myStr = (
            f"ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Active: {self.active}\n"
            f"Billable: {self.billable}\n"
            f"Rate: {self.rate}"
        )

        return myStr
