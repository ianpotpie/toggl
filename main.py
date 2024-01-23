import os
import time
from base64 import b64encode
from datetime import datetime, timedelta, timezone

import requests
from dotenv import load_dotenv

from toggl import Project, TimeEntry

load_dotenv()

BASE_URL = "https://api.track.toggl.com/api/v9/"
API_KEY = os.getenv("API_KEY")
AUTH_BYTES = bytes(f"{API_KEY}:api_token", encoding="ascii")
DEFAULT_HEADERS = {
    "content-type": "application/json",
    "Authorization": "Basic %s" % b64encode(AUTH_BYTES).decode("ascii"),
}
WORKSPACE_ID = os.getenv("WORKSPACE_ID")


def get_project(project_id, workspace_id=WORKSPACE_ID):
    data = requests.get(
        BASE_URL + f"workspaces/{workspace_id}/projects/{project_id}",
        headers=DEFAULT_HEADERS,
    )

    if data.status_code != 200:
        print(f"Failed to fetch data: {data.status_code}")
        return

    return Project(**data.json())


def get_entries(start=None, end=None, meta=True):
    params = {"meta": meta}

    end = datetime.now() if end is None else end
    start_rfc3339 = start.astimezone(timezone.utc).isoformat()
    end_rfc3339 = end.astimezone(timezone.utc).isoformat()

    if start is None:
        params["before"] = end_rfc3339
    else:
        params["start_date"] = start_rfc3339
        params["end_date"] = end_rfc3339

    data = requests.get(
        BASE_URL + "me/time_entries", headers=DEFAULT_HEADERS, params=params
    )

    if data.status_code != 200:
        print(f"Failed to fetch data: {data.status_code}")
        return

    return [TimeEntry(**entry) for entry in data.json()]


def main():
    prev_day = datetime.now() - timedelta(days=1)
    data = get_entries(start=prev_day)
    for entry in sorted(data, key=lambda x: x.start):
        print(entry)
        print()

    project_ids = {entry.project_id for entry in data}

    for project_id in project_ids:
        time.sleep(1)
        print(get_project(project_id))
        print()


if __name__ == "__main__":
    main()
