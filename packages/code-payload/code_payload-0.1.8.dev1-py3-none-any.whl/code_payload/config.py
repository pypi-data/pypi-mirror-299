# src/code_payload/config.py

import logging
import os
from pathlib import Path
from typing import Optional

from omegaconf import OmegaConf
from rich.console import Console
from rich.logging import RichHandler
from rich.pretty import pprint

console = Console()

def load_config(config_path: Optional[str] = None) -> OmegaConf:
    """
    Load configuration from a YAML file, environment variables, and optionally merge with CLI arguments.

    This function first attempts to load a configuration file specified by `config_path`. If not provided,
    it searches for a default configuration file. The loaded configuration is then merged with environment
    variables prefixed with 'CODE_PAYLOAD' and any command-line interface (CLI) arguments.

    Args:
        config_path (Optional[str]): Path to the YAML configuration file. If not provided, a default file is searched for.

    Returns:
        OmegaConf: The merged configuration object containing settings from the YAML file, environment variables, and CLI arguments.

    Raises:
        FileNotFoundError: If the specified or default configuration file is not found.

    Example:
        ```python
        from code_payload.config import load_config

        config = load_config("path/to/config.yaml")
        print(config.project.root)
        ```

    <!-- Example Test:
    >>> from code_payload.config import load_config
    >>> config = load_config("src/code_payload/default_config.yaml")
    >>> assert isinstance(config, (DictConfig, ListConfig))
    >>> assert config.project.root == "./"
    >>> assert config.file_handling.max_file_size == 100000
    -->
    """
    if config_path is None:
        console.log("No config specified.. searching for configuration.")
        config_path = find_config_file()
        console.log(f"Config found at {config_path}")

    if config_path and Path(config_path).exists():
        config = OmegaConf.load(config_path)
    else:
        console.print("[yellow]Config file not found. Exiting.[/yellow]")
        raise FileNotFoundError("Configuration file not found.")

    home_path = find_config_file('.code-payload.yaml')
    if home_path:
        console.log(f"Config found at {home_path}")
        home_conf = OmegaConf.load(home_path)

    env_conf = load_env_config(prefix="CODE_PAYLOAD")
    cli_conf = OmegaConf.from_cli()
    config = OmegaConf.merge(config, home_conf, env_conf, cli_conf)

    pprint(config)
    return config

def find_config_file(filename: str = "default_config.yaml") -> Optional[str]:
    """
    Find the configuration file in the current directory or the user's home directory.

    This function searches for a configuration file in the directory of the running script or
    in the user's home directory.

    Args:
        filename (str): The name of the configuration file to search for. Default is 'default_config.yaml'.

    Returns:
        Optional[str]: The path to the configuration file if found, otherwise None.

    Example:
        ```python
        from code_payload.config import find_config_file

        config_file = find_config_file("my_config.yaml")
        print(config_file)  # Outputs the path to 'my_config.yaml' if found, else None
        ```

    <!-- Example Test:
    >>> from code_payload.config import find_config_file
    >>> config_file = find_config_file("non_existent_config.yaml")
    >>> assert config_file is None
    -->
    """
    script_dir = Path(__file__).resolve().parent
    config_path = script_dir / filename
    if config_path.exists():
        return str(config_path)

    home_config = Path.home() / filename
    if home_config.exists():
        return str(home_config)

    return None

def load_env_config(prefix: str) -> OmegaConf:
    """
    Load environment variables and merge them into an OmegaConf object.

    Args:
        prefix (str): The prefix used to filter environment variables.

    Returns:
        OmegaConf: The configuration object with environment variables.

    Example:
        ```python
        from code_payload.config import load_env_config

        env_config = load_env_config("CODE_PAYLOAD")
        print(env_config)
        ```

    <!-- Example Test:
    >>> from code_payload.config import load_env_config
    >>> env_config = load_env_config("CODE_PAYLOAD")
    >>> assert isinstance(env_config, OmegaConf)
    -->
    """
    env_config = {}
    prefix = prefix.upper() + "_"

    for key, value in os.environ.items():
        if key.startswith(prefix):
            config_key = key[len(prefix):].lower().replace("_", ".")
            env_config[config_key] = parse_env_value(value)

    return OmegaConf.create(env_config)

def parse_env_value(value: str):
    """Parses a string value from an environment variable into the appropriate data type.

    This function attempts to convert the environment variable value into a list, integer,
    float, or boolean, depending on its format.

    Args:
        value (str): The environment variable value to parse.

    Returns:
        Any: The parsed value, which could be a list, int, float, bool, or str.

    Example:
        ```python
        from code_payload.config import parse_env_value

        value = parse_env_value("true")
        print(value)  # Outputs: True
        ```

    <!-- Example Test:
    >>> def test_parse_env_value():
    >>> assert parse_env_value("true") is True
    >>> assert parse_env_value("123") == 123
    >>> assert parse_env_value("1.23") == 1.23
    >>> assert parse_env_value("a,b,c") == ["a", "b", "c"]
    -->
    """
    if "," in value:
        return value.split(",")

    if value.isdigit():
        return int(value)
    try:
        return float(value)
    except ValueError:
        pass
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    return value

def setup_logging(config: OmegaConf):
    """Set up logging configuration using RichHandler.

    This function configures logging with a format and tracebacks enhanced by Rich,
    based on the logging level specified in the configuration.

    Args:
        config (OmegaConf): The configuration object that contains the logging settings.

    Example:
        ```python
        from code_payload.config import setup_logging
        from omegaconf import OmegaConf

        config = OmegaConf.create({"logging": {"level": "INFO"}})
        setup_logging(config)
        ```

    <!--
    Example Test:
    >>> def test_setup_logging():
    >>> config = OmegaConf.create({"logging": {"level": "DEBUG"}})
    >>> setup_logging(config)
    >>> logger = logging.getLogger()
    >>> assert logger.level == logging.DEBUG
    -->
    """
    level = getattr(logging, config.logging.level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
