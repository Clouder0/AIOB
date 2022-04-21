
from dynaconf import Dynaconf, Validator

settings = Dynaconf(
    envvar_prefix="AIOB",
    settings_files=['settings.toml'],
    validators=[Validator("db_path", default="db.json"), ],
)
