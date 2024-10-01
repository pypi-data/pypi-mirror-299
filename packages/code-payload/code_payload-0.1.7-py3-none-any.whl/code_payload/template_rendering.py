# src/code_payload/template_rendering.py

import logging
import os
from typing import Optional

from jinja2 import Environment, FileSystemLoader, Template


def render_template(template_input: Optional[str] = None, template_path: Optional[str] = None, **kwargs) -> str:
    """
    Render a Jinja2 template with the given context.

    This function loads and renders a Jinja2 template specified by `template_input`. If a file path is provided,
    it attempts to load the template from that path; otherwise, it treats the input as a raw template string.
    The template is rendered using the keyword arguments provided.

    Args:
        template_input (Optional[str]): The template file name or raw template string to be rendered.
        template_path (Optional[str]): The path to the directory containing the template files.
        **kwargs: Additional context variables to pass to the template.

    Returns:
        str: The rendered template as a string.

    Raises:
        Exception: If there is an error during template rendering, an empty string is returned, and the error is logged.

    Example:
        ```python
        from code_payload.template_rendering import render_template

        context = {"project_name": "Code Payload"}
        rendered = render_template(template_input="Hello {{ project_name }}!", **context)
        print(rendered)  # Outputs: "Hello Code Payload!"
        ```

    <!-- Example Test:
    >>> from code_payload.template_rendering import render_template
    >>> context = {"project_name": "Code Payload"}
    >>> rendered = render_template(template_input=None, **context)
    >>> assert rendered == ""
    -->
    """
    try:
        # If template_input is None or empty, return an empty string
        if not template_input:
            return ""

        # Adjust the template path to point to the correct directory
        if template_path is None:
            template_path = os.path.join(os.path.dirname(__file__), 'templates')

        # Initialize the Jinja2 environment
        env = Environment(loader=FileSystemLoader(searchpath=template_path))

        # Determine if template_input is a file or a raw template string
        if os.path.exists(os.path.join(template_path, template_input)):
            template = env.get_template(template_input)
        else:
            template = Template(template_input)

        return template.render(**kwargs)

    except Exception as e:
        logging.error(f"Error rendering template: {e}")
        return ""
