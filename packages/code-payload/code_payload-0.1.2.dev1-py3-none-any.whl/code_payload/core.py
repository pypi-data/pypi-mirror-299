# src/code_payload/core.py

import logging
from typing import Optional

from omegaconf import OmegaConf

from code_payload.file_handling import compress_content, walk_directory
from code_payload.models import ProjectStructure
from code_payload.summarization import summarize_content

logger = logging.getLogger(__name__)

def main(config: OmegaConf, render: bool = True, render_args: dict = None) -> Optional[ProjectStructure]:
    """
    Main function to process the project structure and optionally render a template.

    This function walks through the project directory, summarizes file contents based on token limits,
    compresses the content to remove duplicates, and optionally renders a template with the processed
    project structure.

    Args:
        config (OmegaConf): The configuration object containing settings for file handling, token limits, and output.
        render (bool): Flag to determine whether to render a template with the processed project structure. Default is True.
        render_args (dict): Additional arguments for template rendering, if any.

    Returns:
        Optional[ProjectStructure]: The processed project structure if successful, None if an error occurred.

    Example:
        ```python
        from code_payload.config import load_config
        from code_payload.core import main

        config = load_config("path/to/config.yaml")
        project_structure = main(config)
        print(project_structure)
        ```

    <!-- Example Test:
    >>> from omegaconf import OmegaConf
    >>> from code_payload.core import main
    >>> config = OmegaConf.create({
    ...     "project": {"root": "/path/to/project"},
    ...     "file_handling": {"include": {"extensions": [".py", ".md"]}},
    ...     "tokens": {"max_tokens": 100},
    ... })
    >>> project_structure = main(config)
    >>> assert project_structure is not None
    -->
    """
    try:
        # Walk the directory and get the project structure
        project_structure = walk_directory(config)

        # Summarize content based on token limits
        for file in project_structure.files:
            if file.content:
                file.content = summarize_content(file.content, config.tokens.max_tokens)

        # Compress content to remove duplicates
        project_structure = compress_content(project_structure)

        # Return the project structure as JSON or any other desired format
        return project_structure

    except Exception:
        logger.exception("An unexpected error occurred.")
        return None
