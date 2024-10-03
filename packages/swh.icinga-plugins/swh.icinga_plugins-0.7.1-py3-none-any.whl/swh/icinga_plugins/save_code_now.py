# Copyright (C) 2021-2024  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import random
import time
from typing import Dict, List, Union

import requests

from .base_check import BaseCheck

REPORT_MSG = "Save code now request for origin"

WAITING_STATUSES = ("pending", "scheduled", "running")


class SaveCodeNowCheck(BaseCheck):
    TYPE = "SAVECODENOW"
    DEFAULT_WARNING_THRESHOLD = 60
    DEFAULT_CRITICAL_THRESHOLD = 120

    def __init__(
        self, obj: Dict, origin: Union[str, List[str]], visit_type: str
    ) -> None:
        super().__init__(obj, application="scn")
        if isinstance(origin, list):
            origin = random.choice(origin)
        self.api_url = obj["swh_web_url"].rstrip("/")
        self.poll_interval = obj["poll_interval"]
        self.origin = origin
        self.visit_type = visit_type

        self.register_prometheus_gauge("duration", "seconds", ["status"])
        self.register_prometheus_gauge("status", "")

    @staticmethod
    def api_url_scn(root_api_url: str, origin: str, visit_type: str) -> str:
        """Compute the save code now api url for a given origin"""
        return f"{root_api_url}/api/1/origin/save/{visit_type}/url/{origin}/"

    def main(self) -> int:
        """Scenario description:

        1. Requests a save code now request via the api for the given origin (or
        an origin picked at random in the list) with type self.visit_type.

        2. Polling regularly at self.poll_interval seconds the completion status.

        3. When either succeeded, failed or threshold exceeded, report approximate time
        of completion. This will warn if thresholds are exceeded.

        """
        start_time: float = time.time()
        total_time: float = 0.0
        scn_url = self.api_url_scn(self.api_url, self.origin, self.visit_type)
        response = requests.post(scn_url)
        assert response.status_code == 200, (response, response.text)

        result: Dict = response.json()

        status_key = "save_task_status"
        request_date = result["save_request_date"]
        origin_info = (self.visit_type, self.origin)

        while result[status_key] in WAITING_STATUSES:
            time.sleep(self.poll_interval)
            response = requests.get(scn_url)
            assert (
                response.status_code == 200
            ), f"Unexpected response: {response}, {response.text}"
            raw_result: List[Dict] = response.json()
            assert len(raw_result) > 0, f"Unexpected result: {raw_result}"

            if len(raw_result) > 1:
                # retrieve only the one status result we are interested in
                result = next(
                    filter(lambda r: r["save_request_date"] == request_date, raw_result)
                )
            else:
                result = raw_result[0]

            # this because the api can return multiple entries for the same origin
            assert result["save_request_date"] == request_date

            total_time = time.time() - start_time

            if total_time > self.critical_threshold:
                self.print_result(
                    "CRITICAL",
                    f"{REPORT_MSG} {origin_info} took more than {total_time:.2f}s "
                    f'and has status: {result["save_task_status"]}.',
                    total_time=total_time,
                )
                self.collect_prometheus_metric("duration", total_time, ["timeout"])
                self.collect_prometheus_metric("status", 2)
                return 2

        if result[status_key] == "succeeded":
            (status_code, status) = self.get_status(total_time)
            self.print_result(
                status,
                f"{REPORT_MSG} {origin_info} took {total_time:.2f}s and succeeded.",
                total_time=total_time,
            )
            self.collect_prometheus_metric("duration", total_time, ["succeeded"])
            self.collect_prometheus_metric("status", status_code)
            return status_code
        elif result[status_key] == "failed":
            self.print_result(
                "CRITICAL",
                f"{REPORT_MSG} {origin_info} took {total_time:.2f}s and failed.",
                total_time=total_time,
            )
            self.collect_prometheus_metric("duration", total_time, ["failed"])
            self.collect_prometheus_metric("status", 2)
            return 2
        else:
            self.print_result(
                "CRITICAL",
                f"{REPORT_MSG} {origin_info} took {total_time:.2f}s "
                "and resulted in unsupported status: "
                f"{result['save_request_status']} ; {result[status_key]}.",
                total_time=total_time,
            )
            self.collect_prometheus_metric("duration", total_time, ["failed"])
            self.collect_prometheus_metric("status", 2)
            return 2
