import pytest
from omegaconf import OmegaConf

from src.code_payload.config import find_config_file, load_config
from src.code_payload.core import main as process_main


def test_main(tmp_path):
    # Create a simple directory structure
    (tmp_path / "file1.py").write_text("def foo(): pass")
    (tmp_path / "file2.md").write_text("# Title")

    # Set up a simple config
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {
            "exclude": {"extensions": []},
            "include": {"extensions": [".py", ".md"]},
            "max_file_size": 100000,
            "max_summary_length": 100
        },
        "output": {"file": "output.json"},
        "tokens": {"max_tokens": 100},
    })

    # Run the main process
    project_structure = process_main(config)

    assert project_structure is not None
    assert len(project_structure.files) == 2
    assert project_structure.files[0].path.endswith("file1.py")
    assert project_structure.files[1].path.endswith("file2.md")

def test_main_no_files(tmp_path):
    """Test main function when there are no files in the directory."""
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {
            "exclude": {"extensions": []},
            "include": {"extensions": [".py", ".md"]},
            "max_file_size": 100000,
            "max_summary_length": 100
        },
        "tokens": {"max_tokens": 100},
        "output": {"file": "output.json"}
    })

    project_structure = process_main(config)
    assert project_structure is not None
    assert len(project_structure.files) == 0

def test_main_with_empty_file(tmp_path):
    """Test main function when a file is empty."""
    empty_file = tmp_path / "empty_file.py"
    empty_file.write_text("")

    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {
            "exclude": {"extensions": []},
            "include": {"extensions": [".py"]},
            "max_file_size": 100000,
            "max_summary_length": 100
        },
        "tokens": {"max_tokens": 100},
        "output": {"file": "output.json"}
    })

    project_structure = process_main(config)
    assert project_structure is not None
    assert len(project_structure.files) == 1
    assert project_structure.files[0].content is None

def test_main_with_invalid_directory():
    config = OmegaConf.create({
        "project": {"root": "/invalid/path"},
        "file_handling": {"include": {"extensions": [".py"]}}
    })
    project_structure = process_main(config)
    assert project_structure is None

def test_load_config_with_invalid_path_and_environment(monkeypatch):
    monkeypatch.setenv('CODE_PAYLOAD_PROJECT_ROOT', '/invalid/path')
    with pytest.raises(FileNotFoundError):
        load_config(config_path="non_existent_config.yaml")

def test_find_config_file_edge_cases(monkeypatch, tmp_path):
    # Simulate no HOME directory
    monkeypatch.delenv('HOME', raising=False)
    config_file = find_config_file()
    assert config_file is None
