# Copyright 2022, Red Hat, Inc.
# SPDX-License-Identifier: LGPL-2.1-or-later

from openscap_report.dataclasses import asdict, dataclass

from .cpe_logical_test import LogicalTest


@dataclass
class Platform:
    platform_id: str
    logical_test: LogicalTest
    title: str = ""
    result: str = ""

    def as_dict(self):
        return asdict(self)
