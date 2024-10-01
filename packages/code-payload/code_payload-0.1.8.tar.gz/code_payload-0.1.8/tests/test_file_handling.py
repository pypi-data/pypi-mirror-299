import tempfile
from pathlib import Path

import pytest
from omegaconf import OmegaConf

from src.code_payload.file_handling import (
    extract_content,
    is_text_file,
    save_json_output,
    should_include_file,
    walk_directory,
)
from src.code_payload.models import FileContent, ProjectStructure


def test_extract_content(tmp_path):
    # Create a small text file
    text_file = tmp_path / "test.txt"
    text_file.write_text("This is a test file.")

    # Test extraction
    content = extract_content(text_file, max_file_size=100)
    assert content == "This is a test file."

    # Test extraction with a max file size smaller than the content
    content_truncated = extract_content(text_file, max_file_size=10)
    assert content_truncated == "This is a "

    # Test with a binary file
    binary_file = tmp_path / "test.bin"
    binary_file.write_bytes(b'\x00\x01\x02\x03')
    content_binary = extract_content(binary_file, max_file_size=100)
    assert content_binary is None  # Assuming binary files should return None

def test_should_include_file():
    config = OmegaConf.create({
        "file_handling": {
            "exclude": {"extensions": [".log"]},
            "include": {"extensions": [".py", ".md"]}
        }
    })

    # Test exclusion
    file_to_exclude = Path("somefile.log")
    assert not should_include_file(file_to_exclude, config)

    # Test inclusion
    file_to_include = Path("somefile.py")
    assert should_include_file(file_to_include, config)

    # Test default inclusion (not explicitly listed in include/exclude)
    file_to_include_default = Path("somefile.txt")
    assert should_include_file(file_to_include_default, config) is False

def test_walk_directory(tmp_path):
    # Create some files and directories
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1/file1.py").write_text("print('Hello')")
    (tmp_path / "dir1/file2.md").write_text("# Markdown File")

    # Set up a simple config
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {
            "exclude": {"extensions": []},
            "include": {"extensions": [".py", ".md"]},
            "max_file_size": 100000,
            "max_summary_length": 100
        },
        "output": {"file": "output.json"}
    })

    # Run the directory walk
    project_structure = walk_directory(config)

    assert len(project_structure.files) == 2
    assert project_structure.files[0].path.endswith("file1.py")
    assert project_structure.files[1].path.endswith("file2.md")

def test_extract_content_nonexistent_file():
    """Test extract_content raises an error when the file does not exist."""
    non_existent_file = Path("non_existent_file.txt")
    content = extract_content(non_existent_file, max_file_size=100)
    assert content is None

def test_is_text_file_with_uncommon_extension():
    """Test is_text_file correctly identifies uncommon text file extensions."""

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a temporary .rst file with text content
        rst_file = Path(tmpdirname) / "example.rst"
        rst_file.write_text("This is a reStructuredText file.")

        # Check if the .rst file is correctly identified as a text file
        assert is_text_file(rst_file) is True

def test_is_text_file_with_binary_content():
    """Test is_text_file correctly identifies a binary file."""

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a temporary binary file
        binary_file = Path(tmpdirname) / "example.bin"
        binary_file.write_bytes(b'\x00\x01\x02\x03')

        # Check if the binary file is correctly identified as not a text file
        assert is_text_file(binary_file) is False

def test_is_text_file_with_text_extension():
    """Test is_text_file correctly identifies a text file by extension."""

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Create a temporary .txt file with text content
        txt_file = Path(tmpdirname) / "example.txt"
        txt_file.write_text("This is a plain text file.")

        # Check if the .txt file is correctly identified as a text file
        assert is_text_file(txt_file) is True

def test_extract_content_with_large_file(tmp_path):
    large_file = tmp_path / "large_file.txt"
    large_file.write_text("A" * 200000)
    content = extract_content(large_file, max_file_size=100)
    assert content == "A" * 100

def test_walk_directory_with_symlink(tmp_path):
    (tmp_path / "dir1").mkdir()
    (tmp_path / "dir1/file1.py").write_text("print('Hello')")
    (tmp_path / "dir2").mkdir()
    symlink_path = tmp_path / "dir2/symlink"
    symlink_path.symlink_to(tmp_path / "dir1/file1.py")

    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}}
    })
    project_structure = walk_directory(config)
    assert len(project_structure.files) == 1

def test_extract_content_with_permission_error(monkeypatch, tmp_path):
    # Simulate a permission error on a file
    restricted_file = tmp_path / "restricted.txt"
    restricted_file.write_text("This file has restricted permissions.")
    restricted_file.chmod(0o000)  # No permissions

    with pytest.raises(PermissionError):
        extract_content(restricted_file, max_file_size=100)

    restricted_file.chmod(0o644)  # Reset permissions for cleanup

def test_walk_directory_with_non_existent_path():
    config = OmegaConf.create({
        "project": {"root": "/non/existent/path"},
        "file_handling": {"include": {"extensions": [".py"]}}
    })
    with pytest.raises(FileNotFoundError):
        walk_directory(config)

def test_extract_content_with_special_characters(tmp_path):
    special_file = tmp_path / "special_file.py"
    special_file.write_text("print('Special characters: ñ, ö, ç')")
    content = extract_content(special_file, max_file_size=100)
    assert "Special characters" in content

def test_walk_directory_with_hidden_files(tmp_path):
    (tmp_path / ".hidden").mkdir()
    hidden_file = tmp_path / ".hidden/hidden.py"
    hidden_file.write_text("print('Hidden file')")

    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
    })
    project_structure = walk_directory(config)
    assert len(project_structure.files) == 1
    assert hidden_file.name in project_structure.files[0].path

def test_is_text_file_with_uncommon_mime_type(tmp_path):
    uncommon_file = tmp_path / "example.custom"
    uncommon_file.write_text("This is a file with an uncommon extension.")
    assert is_text_file(uncommon_file) is True  # Check with uncommon MIME type

def test_walk_directory_with_special_files(tmp_path):
    special_file = tmp_path / "special.py"
    special_file.write_text("# Special file")
    hidden_file = tmp_path / ".hidden.py"
    hidden_file.write_text("# Hidden file")

    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
    })
    project_structure = walk_directory(config)
    assert len(project_structure.files) == 1  # Only special.py should be included

def test_is_text_file_edge_cases(tmp_path):
    # Test a file with an uncommon extension but valid text content
    uncommon_file = tmp_path / "example.cfg"
    uncommon_file.write_text("key=value\n")
    assert is_text_file(uncommon_file) is True

    # Test a binary file that might not be detected correctly
    binary_file = tmp_path / "example.bin"
    binary_file.write_bytes(b'\x89PNG\r\n\x1a\n')
    assert is_text_file(binary_file) is False

def test_walk_directory_with_symlinks(tmp_path):
    # Create a directory structure with symlinks
    real_dir = tmp_path / "real_dir"
    real_dir.mkdir()
    symlink_dir = tmp_path / "symlink_dir"
    symlink_dir.symlink_to(real_dir)
    (real_dir / "file.py").write_text("print('Hello World')")

    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
    })
    project_structure = walk_directory(config)
    assert len(project_structure.files) == 1
    assert project_structure.files[0].path.endswith("file.py")


def test_save_json_output_creates_directory(tmp_path):
    project_structure = ProjectStructure(root=str(tmp_path), files=[FileContent(path="example.py", content="print('Hello World')")])
    output_path = tmp_path / "nonexistent" / "output.json"

    save_json_output(project_structure, output_path)

    assert output_path.exists()

def test_save_json_output_with_existing_directory(tmp_path):
    project_structure = ProjectStructure(root=str(tmp_path), files=[FileContent(path="example.py", content="print('Hello World')")])
    output_dir = tmp_path / "existing_dir"
    output_dir.mkdir()
    output_path = output_dir / "output.json"

    save_json_output(project_structure, output_path)

    assert output_path.exists()
