import copy
import time
import webbrowser
from typing import Annotated, Any

import toml
import typer
from beaupy import confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from typer_config.loaders import toml_loader

from trainwave_cli.api import Api, CLIConfigSessionStatus
from trainwave_cli.config.config import config
from trainwave_cli.utils import async_command, ensure_api_key

CONFIG_SESSION_POLLING_TIME: Annotated[int, "minutes"] = 20
CONFIG_SESSION_POLLING_SLEEP_TIME: Annotated[int, "seconds"] = 5

app = typer.Typer()


async def _run_setup_guide(existing_config: dict[str, Any]) -> dict[str, Any]:
    typer.echo("Running setup\n")
    api_client = Api(config.api_key, config.endpoint)

    _existing_config = copy.deepcopy(existing_config)
    if _existing_config.get("env_vars"):
        vars = _existing_config.pop("env_vars")
        _existing_config["env_vars"] = [{"key": k, "value": v} for k, v in vars.items()]

    url, session_token = await api_client.create_cli_config_session(_existing_config)
    webbrowser.open_new_tab(url)

    end_polling_at = time.time() + 60 * CONFIG_SESSION_POLLING_TIME
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Awaiting config...", total=None)

        while time.time() < end_polling_at:
            status, new_config = await api_client.check_cli_config_session_status(
                session_token
            )
            if status == CLIConfigSessionStatus.COMPLETE:
                # convert back the env vars
                if new_config and new_config.get("env_vars"):
                    vars = new_config.pop("env_vars")
                    new_config["env_vars"] = {var["key"]: var["value"] for var in vars}

                return new_config or {}

            time.sleep(CONFIG_SESSION_POLLING_SLEEP_TIME)

    return {}


@app.callback(invoke_without_command=True)
@async_command
@ensure_api_key
async def default(
    config: Annotated[str | None, typer.Argument()] = None,
    accept: Annotated[bool, "Accept overwrite of config"] = False,
) -> None:
    config_path = "trainwave.toml"
    if config:
        config_path = config

    try:
        existing_config = toml_loader(config_path)
    except FileNotFoundError:
        existing_config = {}

    new_config = await _run_setup_guide(existing_config or {})

    if new_config:
        confirmed = accept or confirm(
            f"You already have a config file({config_path}). Do you want to overwrite it?"
        )

        if confirmed:
            with open(config_path, "w") as f:
                # Merge and dump
                toml.dump(existing_config | new_config, f)

            typer.echo(f"Config file saved to {config_path}.")
        else:
            typer.echo("Config file not saved to file. \n")

            typer.echo("Config: \n")
            typer.echo(toml.dumps(existing_config | new_config))
