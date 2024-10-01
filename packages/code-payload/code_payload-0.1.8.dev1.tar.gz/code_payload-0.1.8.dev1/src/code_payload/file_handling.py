# src/code_payload/file_handling.py

import json
import logging
import mimetypes
from collections import defaultdict
from pathlib import Path
from typing import Optional

import chardet
from omegaconf import OmegaConf

from code_payload.models import FileContent, ProjectStructure
from code_payload.summarization import summarize_content

logger = logging.getLogger(__name__)

def format_as_json(project_structure: ProjectStructure) -> str:
    """
    Convert the project structure into a JSON string.

    This function serializes the given ProjectStructure object into a JSON-formatted string.

    Args:
        project_structure (ProjectStructure): The project structure to serialize.

    Returns:
        str: The JSON representation of the project structure.

    Example:
        ```python
        from code_payload.models import ProjectStructure, FileContent
        from code_payload.file_handling import format_as_json

        files = [FileContent(path="example.py", content="print('Hello World')")]
        project_structure = ProjectStructure(root="/path/to/project", files=files)
        json_output = format_as_json(project_structure)
        print(json_output)  # Outputs the JSON string
        ```

    <!-- Example Test:
    >>> from code_payload.models import ProjectStructure, FileContent
    >>> from code_payload.file_handling import format_as_json
    >>> files = [FileContent(path="example.py", content="print('Hello World')")]
    >>> project_structure = ProjectStructure(root="/path/to/project", files=files)
    >>> json_output = format_as_json(project_structure)
    >>> assert json.loads(json_output)["root"] == "/path/to/project"
    -->
    """
    return json.dumps(project_structure.model_dump(by_alias=True), separators=(",", ":"))

def save_json_output(project_structure: ProjectStructure, output_path: Path) -> None:
    """
    Save the project structure as a minified JSON file, ensuring the output directory exists.

    This function formats the given `ProjectStructure` object into a JSON string and writes it to the
    specified `output_path`. It ensures that the output directory is created if it does not already exist.

    Args:
        project_structure (ProjectStructure): The project structure to be saved.
        output_path (Path): The path where the output JSON file should be saved.

    Raises:
        OSError: If there is an issue with creating directories or writing to the file.

    Example:
        ```python
        from pathlib import Path
        from code_payload.models import ProjectStructure, FileContent
        from code_payload.file_handling import save_json_output

        project_structure = ProjectStructure(
            root="/path/to/project",
            files=[FileContent(path="example.py", content="print('Hello World')")]
        )
        output_path = Path("/path/to/output/output.json")

        save_json_output(project_structure, output_path)
        print(f"Output saved at {output_path}")
        ```

    <!-- Example Test:
    >>> from pathlib import Path
    >>> from code_payload.models import ProjectStructure, FileContent
    >>> from code_payload.file_handling import save_json_output
    >>> tmp_path = Path("/tmp/code_payload_test")
    >>> project_structure = ProjectStructure(
    ...     root=str(tmp_path),
    ...     files=[FileContent(path="example.py", content="print('Hello World')")]
    ... )
    >>> output_path = tmp_path / "nonexistent" / "output.json"
    >>> save_json_output(project_structure, output_path)
    >>> assert output_path.exists()
    >>> with open(output_path, "r") as f:
    ...     data = f.read()
    >>> assert "example.py" in data
    -->
    """
    try:
        output_dir = output_path.parent

        # Ensure the directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Format the project structure as JSON
        json_output = format_as_json(project_structure)

        # Write the JSON output to the specified file
        with open(output_path, 'w') as f:
            f.write(json_output)

        logger.info(f"Output successfully saved to {output_path}")

    except Exception as e:
        logger.error(f"Failed to save output to {output_path}: {e}")
        raise

def is_text_file(file_path: Path) -> bool:
    """
    Checks if the file is a text file based on its extension and MIME type.

    This function determines whether a file is a text file by checking its file extension
    against common text file types and validating its MIME type if the extension is uncommon.

    Args:
        file_path (Path): The path to the file to check.

    Returns:
        bool: True if the file is identified as a text file, False otherwise.

    Example:
        ```python
        import tempfile
        from pathlib import Path
        from code_payload.file_handling import is_text_file

        # Create a temporary directory and files within it
        with tempfile.TemporaryDirectory() as tmpdirname:
            # Create a text file with an uncommon extension
            rst_file = Path(tmpdirname) / "example.rst"
            rst_file.write_text("This is a reStructuredText file.")

            # Check if the .rst file is correctly identified as a text file
            print(is_text_file(rst_file))  # Expected output: True

            # Create a binary file
            binary_file = Path(tmpdirname) / "example.bin"
            binary_file.write_bytes(b'\x00\x01\x02\x03')

            # Check if the binary file is correctly identified as not a text file
            print(is_text_file(binary_file))  # Expected output: False
        ```

    <!-- Example Test:
    >>> import tempfile
    >>> from pathlib import Path
    >>> from code_payload.file_handling import is_text_file
    >>> with tempfile.TemporaryDirectory() as tmpdirname:
    ...     rst_file = Path(tmpdirname) / "example.rst"
    ...     rst_file.write_text("This is a reStructuredText file.")
    ...     assert is_text_file(rst_file) is True
    ...     binary_file = Path(tmpdirname) / "example.bin"
    ...     binary_file.write_bytes(b'\x00\x01\x02\x03')
    ...     assert is_text_file(binary_file) is False
    -->
    """
    text_extensions = {
        ".txt", ".md", ".py", ".js", ".html", ".css", ".json",
        ".xml", ".yaml", ".yml", ".ini", ".cfg", ".rst", ".toml"
    }

    # If the file extension is recognized as a text file type, return True
    if file_path.suffix.lower() in text_extensions:
        return True

    # Check the MIME type as a fallback
    mime_type, _ = mimetypes.guess_type(file_path)
    if mime_type and mime_type.startswith('text'):
        return True

    return False

def is_binary(file_path: Path, max_file_size: int) -> bool:
    """Determine if a file is binary by analyzing its content.

    This function reads a portion of the file's content (up to `max_file_size` bytes) and checks if the file
    is binary. It does this by detecting if the content contains non-text characters or if no valid encoding
    is found using `chardet`.

    Args:
        file_path (Path): The path to the file that needs to be checked.
        max_file_size (int): The maximum number of bytes to read from the file for analysis.

    Returns:
        bool: True if the file is detected as binary, False otherwise.

    Raises:
        Exception: If there is an error reading the file, the function assumes the file is binary and logs the error.

    Example:
        ```python
        from pathlib import Path
        from code_payload.file_handling import is_binary

        result = is_binary(Path("path/to/file.txt"), max_file_size=1000)
        print(result)  # Outputs: False (if text) or True (if binary)
        ```

    Example Test:
        ```python
        def test_is_binary(tmp_path):
            binary_file = tmp_path / "test.bin"
            binary_file.write_bytes(b'\x00\x01\x02\x03')
            assert is_binary(binary_file, max_file_size=1000) is True

            text_file = tmp_path / "test.txt"
            text_file.write_text("This is a test file.")
            assert is_binary(text_file, max_file_size=1000) is False
        ```
    """
    try:
        with file_path.open('rb') as f:
            raw_content = f.read(max_file_size)
        detected = chardet.detect(raw_content)
        detected_binary: bool = detected['encoding'] is None
        binary_text_characters = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
        detected_binary_text: bool = bool(raw_content.translate(None, binary_text_characters))

        return True if any([detected_binary, detected_binary_text]) else False

    except Exception as e:
        logger.error(f"Error detecting if file is binary: {e}")
        return True  # If there's an error, assume it's binary

def extract_content(file_path: Path, max_file_size: int) -> Optional[str]:
    """
    Extract the content of a file up to a specified maximum file size.

    This function reads the content of a file as a string, but truncates it if the content exceeds the specified `max_file_size`.

    Args:
        file_path (Path): The path to the file to extract content from.
        max_file_size (int): The maximum file size to read.

    Returns:
        Optional[str]: The content of the file if readable, truncated if necessary. Returns None if the file is not readable as text.

    Example:
        ```python
        from pathlib import Path
        from code_payload.file_handling import extract_content

        content = extract_content(Path("example.txt"), max_file_size=100)
        print(content)  # Outputs the content up to 100 bytes
        ```

    <!-- Example Test:
    >>> from pathlib import Path
    >>> from code_payload.file_handling import extract_content
    >>> content = extract_content(Path("example.txt"), max_file_size=100)
    >>> assert content is not None
    >>> assert len(content) <= 100
    -->
    """
    if is_binary(file_path, max_file_size):
        return None
    try:
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read(max_file_size)
        return content
    except UnicodeDecodeError:
        try:
            with file_path.open("rb") as f:
                raw_content = f.read(max_file_size)
            detected = chardet.detect(raw_content)
            encoding = detected["encoding"] if detected["encoding"] else "utf-8"
            content = raw_content.decode(encoding)
            return content
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return None
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None

def should_include_file(file_path: Path, config: OmegaConf) -> bool:
    """
    Determine if a file should be included based on the configuration settings.

    This function checks the file's extension against the include and exclude lists in the configuration to decide
    whether the file should be included in the processing.

    Args:
        file_path (Path): The path to the file to check.
        config (OmegaConf): The configuration object with include/exclude settings.

    Returns:
        bool: True if the file should be included, False otherwise.

    Example:
        ```python
        from pathlib import Path
        from omegaconf import OmegaConf
        from code_payload.file_handling import should_include_file

        config = OmegaConf.create({
            "file_handling": {
                "include": {"extensions": [".py", ".md"]},
                "exclude": {"extensions": [".log"]}
            }
        })

        include = should_include_file(Path("example.py"), config)
        print(include)  # Outputs: True
        ```

    <!-- Example Test:
    >>> from pathlib import Path
    >>> from omegaconf import OmegaConf
    >>> from code_payload.file_handling import should_include_file
    >>> config = OmegaConf.create({
    ...     "file_handling": {
    ...         "include": {"extensions": [".py", ".md"]},
    ...         "exclude": {"extensions": [".log"]}
    ...     }
    ... })
    >>> assert should_include_file(Path("example.py"), config) is True
    >>> assert should_include_file(Path("example.log"), config) is False
    -->
    """
    if any(part for part in file_path.parts if part.startswith(".") and part != ".github"):
        return False

    if file_path.suffix in config.file_handling.exclude.extensions:
        return False

    if config.file_handling.include.extensions:
        return file_path.suffix in config.file_handling.include.extensions

    return True

def walk_directory(config: OmegaConf) -> ProjectStructure:
    """
    Walk through the project directory and gather the structure based on the configuration.

    This function traverses the directory specified in the `config` and gathers information about the files that match
    the inclusion criteria. The gathered data is returned as a `ProjectStructure` object.

    Args:
        config (OmegaConf): The configuration object with settings for directory walking.

    Returns:
        ProjectStructure: An object representing the structure of the project directory.

    Example:
        ```python
        from omegaconf import OmegaConf
        from code_payload.file_handling import walk_directory

        config = OmegaConf.create({
            "project": {"root": "/path/to/project"},
            "file_handling": {"include": {"extensions": [".py", ".md"]}}
        })

        project_structure = walk_directory(config)
        print(len(project_structure.files))  # Outputs the number of files found
        ```

    <!-- Example Test:
    >>> from omegaconf import OmegaConf
    >>> from code_payload.file_handling import walk_directory
    >>> config = OmegaConf.create({
    ...     "project": {"root": "/path/to/project"},
    ...     "file_handling": {"include": {"extensions": [".py", ".md"]}}
    ... })
    >>> project_structure = walk_directory(config)
    >>> assert len(project_structure.files) > 0
    -->
    """
    files = []
    root_path = Path(config.project.root).resolve()
    logger.info(f"Scanning directory: {root_path}")

    output_file_name = config.output.file  # Get the name of the output file to exclude it

    if not root_path.exists() or not root_path.is_dir():
        logger.error(f"Invalid directory: {root_path}")
        return ProjectStructure(root=str(root_path), files=[])

    for file_path in root_path.rglob("*"):
        if file_path.is_file() and should_include_file(file_path, config):
            relative_path = file_path.relative_to(root_path)

            # Exclude the output file itself
            if str(relative_path) == output_file_name:
                continue

            if is_text_file(file_path):
                content = extract_content(file_path, config.file_handling.max_file_size)
                if content:
                    summarized_content = summarize_content(content, config.file_handling.max_summary_length)
                    files.append(FileContent(path=str(relative_path), content=summarized_content))
                else:
                    files.append(FileContent(path=str(relative_path), error="Error reading file"))
            else:
                files.append(FileContent(path=str(relative_path), error="Binary file"))

    logger.info(f"Total files processed: {len(files)}")
    return compress_content(ProjectStructure(root=str(root_path), files=files))

def compress_content(project_structure: ProjectStructure) -> ProjectStructure:
    """
    Compress the content of files in the project structure by removing duplicates.

    This function identifies and removes duplicate file content within the project structure,
    helping to reduce redundancy. Files with empty content are retained in the structure.

    Args:
        project_structure (ProjectStructure): The project structure to compress.

    Returns:
        ProjectStructure: The compressed project structure.

    Example:
        ```python
        from code_payload.file_handling import compress_content
        from code_payload.models import ProjectStructure, FileContent

        files = [
            FileContent(path="file1.py", content="print('Hello World')"),
            FileContent(path="file2.py", content="print('Hello World')"),
            FileContent(path="file3.py", content="")
        ]
        project_structure = ProjectStructure(root="/path/to/project", files=files)
        compressed_structure = compress_content(project_structure)
        print(len(compressed_structure.files))  # Outputs: 2 (if file3.py has unique empty content)
        ```

    <!-- Example Test:
    >>> from code_payload.file_handling import compress_content
    >>> from code_payload.models import ProjectStructure, FileContent
    >>> files = [
    ...     FileContent(path="file1.py", content="print('Hello World')"),
    ...     FileContent(path="file2.py", content="print('Hello World')"),
    ...     FileContent(path="file3.py", content="")
    ... ]
    >>> project_structure = ProjectStructure(root="/path/to/project", files=files)
    >>> compressed_structure = compress_content(project_structure)
    >>> assert len(compressed_structure.files) == 2
    -->
    """
    content_dict = defaultdict(list)
    empty_files = []

    for file in project_structure.files:
        if file.content:
            content_dict[file.content].append(file.path)
        else:
            empty_files.append(file)

    compressed_files = []
    for content, paths in content_dict.items():
        if len(paths) > 1:
            compressed_files.append(FileContent(path=",".join(paths), content=content))
        else:
            compressed_files.append(FileContent(path=paths[0], content=content))

    # Add back files with empty content
    compressed_files.extend(empty_files)

    return ProjectStructure(root=project_structure.root, files=compressed_files)
