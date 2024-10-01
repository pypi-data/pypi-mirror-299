import logging
from typing import Optional

from omegaconf import OmegaConf
from rich.console import Console

from code_payload.core import compress_content
from code_payload.file_handling import walk_directory
from code_payload.models import ProjectStructure
from code_payload.summarization import summarize_content
from code_payload.template_rendering import render_template

console = Console()
logger = logging.getLogger(__name__)

def main(config: OmegaConf, render: bool = True, render_args: dict = None) -> Optional[ProjectStructure]:
    """
    Main function to process a project directory, summarize file contents, compress duplicates,
    and optionally render a template based on the provided configuration.

    This function performs the following steps:
    1. Walks through the project directory specified in the `config`.
    2. Summarizes the content of each file based on the token limits specified in `config.tokens.max_tokens`.
    3. Compresses the content by merging files with identical content.
    4. Optionally renders a template using the processed project structure if the `render` flag is set to True
       and `render_args` is provided.

    Args:
        config (OmegaConf): A configuration object containing settings for file handling, token limits,
            and output options. The configuration should be loaded from a YAML file, environment variables,
            or CLI arguments.
        render (bool): A flag indicating whether to render a template using the processed project structure.
            Defaults to True.
        render_args (dict, optional): A dictionary of additional arguments for template rendering, such as
            `template_input` and `template_path`. If None, rendering is skipped.

    Returns:
        Optional[ProjectStructure]: A `ProjectStructure` object representing the processed project if successful,
            or None if an error occurred.

    Example:
        To process a project directory and render a template, you can use the following code:

        ```python
        from code_payload.config import load_config
        from code_payload.core import main

        config = load_config("path/to/config.yaml")
        render_args = {
            "template_input": "template.j2",
            "template_path": "path/to/templates"
        }
        project_structure = main(config, render=True, render_args=render_args)
        print(project_structure)
        ```

    Example Test:
        The following test ensures that the `main` function processes a directory correctly:

        ```python
        from pathlib import Path
        from omegaconf import OmegaConf
        from code_payload.core import main

        def test_main(tmp_path: Path):
            # Create a simple directory structure
            (tmp_path / "file1.py").write_text("def foo(): pass")
            (tmp_path / "file2.md").write_text("# Title")

            # Set up a simple config
            config = OmegaConf.create({
                "project": {"root": str(tmp_path)},
                "file_handling": {"include": {"extensions": [".py", ".md"]}},
                "tokens": {"max_tokens": 100},
                "logging": {"level": "INFO"},
            })

            # Run the main process
            project_structure = main(config, render=False)

            # Assertions
            assert project_structure is not None
            assert len(project_structure.files) == 2
            assert project_structure.files[0].path.endswith("file1.py")
            assert project_structure.files[1].path.endswith("file2.md")
        ```

    Raises:
        Exception: If any unexpected error occurs during the process, it logs the error and returns None.
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

        # Render template if required
        if render and render_args:
            rendered_output = render_template(
                template_input=render_args.get('template_input'),
                template_path=render_args.get('template_path'),
                project_structure=project_structure
            )
            console.print(rendered_output)

        return project_structure

    except Exception:
        logger.exception("An unexpected error occurred.")
        return None
