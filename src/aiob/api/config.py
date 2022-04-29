"""Config Utility for AIOB."""

from __future__ import annotations

import os

from dynaconf import Dynaconf, Validator


settings = Dynaconf(
    envvar_prefix="AIOB",
    settings_files=[os.getcwd() + "/settings.toml"],
    validators=[
        Validator("db_path", default="db.json"),
    ],
)
