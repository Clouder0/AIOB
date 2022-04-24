import os

from dynaconf import Dynaconf, Validator

# type annotations for dynaconf will be added by version 4.0.0 #TODO
settings = Dynaconf(
    envvar_prefix="AIOB",
    settings_files=[os.getcwd() + '/settings.toml'],
    validators=[Validator("db_path", default="db.json"), ],
)
