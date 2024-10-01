# src/code_payload/models.py

from typing import List, Optional

from pydantic import BaseModel


class FileContent(BaseModel):
    """
    Model representing the content of a file within a project.

    Attributes:
        path (str): The file path.
        content (Optional[str]): The content of the file, if it could be read.
        error (Optional[str]): An error message if the file content could not be read.

    Example:
        ```python
        from code_payload.models import FileContent

        file = FileContent(path="example.py", content="print('Hello World')")
        print(file.path)  # Outputs: example.py
        print(file.content)  # Outputs: print('Hello World')
        ```

    <!-- Example Test:
    >>> from code_payload.models import FileContent
    >>> file = FileContent(path="example.py", content="print('Hello World')")
    >>> assert file.path == "example.py"
    >>> assert file.content == "print('Hello World')"
    -->
    """
    path: str
    content: Optional[str] = None
    error: Optional[str] = None

class ProjectStructure(BaseModel):
    """
    Model representing the structure of a project directory.

    Attributes:
        root (str): The root directory of the project.
        files (List[FileContent]): A list of files within the project, each represented by a FileContent object.

    Example:
        ```python
        from code_payload.models import ProjectStructure, FileContent

        files = [
            FileContent(path="example.py", content="print('Hello World')"),
            FileContent(path="README.md", content="# Project Documentation")
        ]
        project_structure = ProjectStructure(root="/path/to/project", files=files)
        print(project_structure.root)  # Outputs: /path/to/project
        print(len(project_structure.files))  # Outputs: 2
        ```

    <!-- Example Test:
    >>> from code_payload.models import ProjectStructure, FileContent
    >>> files = [
    ...     FileContent(path="example.py", content="print('Hello World')"),
    ...     FileContent(path="README.md", content="# Project Documentation")
    ... ]
    >>> project_structure = ProjectStructure(root="/path/to/project", files=files)
    >>> assert project_structure.root == "/path/to/project"
    >>> assert len(project_structure.files) == 2
    -->
    """
    root: str
    files: List[FileContent]
