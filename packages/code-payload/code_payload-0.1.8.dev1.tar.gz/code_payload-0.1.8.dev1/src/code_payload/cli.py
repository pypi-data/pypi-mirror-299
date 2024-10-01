# src/code_payload/cli.py

import json
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.syntax import Syntax
from rich.theme import Theme

from code_payload.config import load_config, setup_logging
from code_payload.core import main as process_main
from code_payload.file_handling import save_json_output
from code_payload.template_rendering import render_template
from code_payload.models import ProjectStructure

app = typer.Typer()

custom_theme = Theme({
    "json.key": "bold white",
    "json.value.string": "green",
    "json.value.number": "cyan",
    "json.brace": "white",
    "json.comma": "white",
    "json.colon": "white"
})

console = Console(theme=custom_theme)

@app.command()
def cli(
    project_path: Path,
    config_file: Path = None,
    output_file: Path = None,
    log_level: str = "INFO",
    return_prompt: bool = typer.Option(False, help="Whether to return the rendered prompt (default: True)"),
    render_args: Optional[List[str]] = typer.Option(None, help="Additional arguments for rendering the template (e.g., key1=value1,key2=value2)"),
    include_extensions: Optional[List[str]] = typer.Option(None, help="File extensions to include, e.g., .py,.js"),
):
    """
    Command-line interface for processing a project directory and generating a summary.

    This CLI command processes a specified project directory, optionally using a configuration file,
    and outputs a summary based on the provided options. The output can be a rendered template if specified.

    Args:
        project_path (Path): The path to the project directory to process.
        config_file (Path, optional): Path to the configuration file. Defaults to None.
        output_file (Path, optional): Path to the output file. Defaults to None.
        log_level (str, optional): The logging level (e.g., "INFO", "DEBUG"). Defaults to "INFO".
        return_prompt (bool, optional): Whether to return the rendered prompt. Defaults to False.
        render_args (Optional[List[str]], optional): Additional arguments for rendering the template. Defaults to None.
        include_extensions (Optional[List[str]], optional): File extensions to include. Defaults to None.

    Example:
        ```bash
        python src/code_payload/cli.py /path/to/project --log-level DEBUG --include-extensions .py,.md
        ```

    <!-- Example Test:
    >>> from typer.testing import CliRunner
    >>> from code_payload.cli import app
    >>> runner = CliRunner()
    >>> result = runner.invoke(app, ["--help"])
    >>> assert result.exit_code == 0
    >>> assert "Usage" in result.output
    -->
    """
    config = load_config(config_file)
    config.project.root = str(project_path)
    if output_file:
        config.output.file = str(output_file)
    config.logging.level = log_level.upper()

    if include_extensions:
        config.file_handling.include.extensions = include_extensions

    setup_logging(config)

    render_args_dict = {}
    if render_args:
        for arg in render_args:
            key, value = arg.split("=")
            render_args_dict[key] = value

    console.print(f"\n\n📂 Processing directory: {project_path}", style="bold green")

    project_structure: ProjectStructure = process_main(config)

    if return_prompt:
        # Create a combined dictionary with all the necessary keys
        combined_args = {
            **config,  # Include all configuration options
            **(render_args_dict or {}),  # Include render arguments if any
            'project_structure': project_structure  # Pass the project structure to the template
        }

        # Determine the template input, defaulting to 'default.j2'
        template_input = combined_args.pop('template_input', 'default.j2')

        # Pass the combined dictionary as **kwargs to the render function
        rendered_prompt = render_template(
            template_input=template_input,  # Pass the template_input explicitly
            **combined_args  # Pass the rest of the arguments
        )
        # # Rendering the template using the project structure
        # rendered_prompt = render_template(
        #     template_input=render_args_dict.get('template_input', 'default.j2'),
        #     **render_args_dict,
        #     project_structure=project_structure,  # Pass the project structure to the template
        #     **config
        # )
        console.print("\nRendered prompt:", style="bold white")
        console.print(rendered_prompt, style="bold")
    else:
        # Display the JSON structure if no template rendering is requested
        console.print("\nJSON Payload:", style="bold white")
        json_output = project_structure.model_dump_json(by_alias=True, indent=2)  # Serialize manually using json.dumps
        syntax = Syntax(json_output, "json", theme="monokai", line_numbers=False, word_wrap=True)
        console.print(syntax)

    # Optionally save the JSON output to a file
    if output_file:
        save_json_output(project_structure, output_file)
        # with output_file.open("w", encoding="utf-8") as f:
        #     f.write(format_as_json(project_structure))
        console.print(f"\nJSON output saved to: {output_file}", style="bold green")


if __name__ == "__main__":
    app()
