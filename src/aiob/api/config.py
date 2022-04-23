from dynaconf import Dynaconf, Validator  # type: ignore
# type annotations for dynaconf will be added by version 4.0.0 #TODO
settings = Dynaconf(
    envvar_prefix="AIOB",
    settings_files=['settings.toml'],
    validators=[Validator("db_path", default="db.json"), ],
)
