# Copyright 2022, Red Hat, Inc.
# SPDX-License-Identifier: LGPL-2.1-or-later

from typing import Dict

from openscap_report.dataclasses import asdict, dataclass, field


@dataclass
class OvalVariable:
    variable_id: str
    comment: str = ""
    variable_type: str = ""
    variable_data: Dict[str, str] = field(default_factory=dict)

    def as_dict(self):
        return asdict(self)
