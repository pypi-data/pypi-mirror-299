from pathlib import Path

import pytest
from omegaconf import DictConfig, ListConfig
from omegaconf.errors import OmegaConfBaseException

from src.code_payload.config import find_config_file, load_config


def test_load_config_with_invalid_path():
    """Test loading configuration with an invalid path should raise FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_config(config_path="invalid/path/to/config.yaml")

def test_find_config_file_no_file():
    """Test find_config_file returns None when the file is not found."""
    config_file = find_config_file(filename="non_existent_config.yaml")
    assert config_file is None

def test_load_config():
    """Test loading of the configuration file."""
    config = load_config(config_path="src/code_payload/default_config.yaml")

    assert isinstance(config, (ListConfig, DictConfig))
    assert config.project.root == "./"
    assert config.file_handling.max_file_size == 100000
    assert config.output.format == "json"

def test_load_config_with_env_vars(monkeypatch):
    monkeypatch.setenv('CODE_PAYLOAD_PROJECT_ROOT', '/path/to/project')
    config = load_config()
    assert config.project.root == '/path/to/project'

def test_find_config_file_in_home_dir(monkeypatch):
    home_dir = Path.home() / 'default_config.yaml'
    home_dir.write_text('project:\n  root: "./"')
    config_file = find_config_file()
    assert config_file == home_dir

def test_load_config_with_invalid_yaml(monkeypatch, tmp_path):
    # Simulate an invalid YAML file
    invalid_yaml = tmp_path / "invalid_config.yaml"
    invalid_yaml.write_text("project: root: ./")  # Invalid structure

    with pytest.raises(OmegaConfBaseException):
        load_config(config_path=str(invalid_yaml))

def test_find_config_file_in_multiple_locations(monkeypatch):
    monkeypatch.setenv('HOME', '/non/existent/home')
    config_file = find_config_file()
    assert config_file is None

def test_load_config_with_empty_env_var(monkeypatch):
    monkeypatch.setenv('CODE_PAYLOAD_LOGGING_LEVEL', '')
    config = load_config()
    assert config.logging.level == 'INFO'  # Default value

def test_find_config_file_in_empty_directory(tmp_path):
    config_file = find_config_file()
    assert config_file is None  # Should return None if no config file found

def test_load_config_with_partial_env_override(monkeypatch):
    monkeypatch.setenv('CODE_PAYLOAD_PROJECT_ROOT', '/tmp')
    config = load_config()
    assert config.project.root == '/tmp'
    assert config.file_handling.max_file_size == 100000  # Ensure other settings are not overridden

def test_find_config_file_with_custom_filename(tmp_path):
    custom_config = tmp_path / "custom_config.yaml"
    custom_config.write_text("project:\n  root: './'")
    result = find_config_file("custom_config.yaml")
    assert result == str(custom_config)

def test_load_config_with_invalid_logging_level(monkeypatch):
    monkeypatch.setenv('CODE_PAYLOAD_LOGGING_LEVEL', 'INVALID_LEVEL')
    with pytest.raises(ValueError):
        load_config()

def test_find_config_file_with_edge_cases(tmp_path, monkeypatch):
    # Test with an empty home directory
    monkeypatch.setenv('HOME', str(tmp_path))
    config_file = find_config_file()
    assert config_file is None

    # Test with an empty config file
    empty_config = tmp_path / "default_config.yaml"
    empty_config.write_text("")
    with pytest.raises(OmegaConfBaseException):
        load_config(config_path=str(empty_config))
