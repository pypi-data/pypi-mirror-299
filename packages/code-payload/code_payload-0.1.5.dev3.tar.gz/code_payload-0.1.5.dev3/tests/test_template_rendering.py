from src.code_payload.template_rendering import render_template


def test_render_template_with_invalid_template():
    """Test render_template with an invalid template input."""
    context = {"project_name": "Code Payload"}
    rendered = render_template(template_input=None, **context)
    assert rendered == ""

def test_render_template_with_missing_context():
    """Test render_template when required context variables are missing."""
    rendered = render_template(template_input="Hello {{ project_name }}!")
    assert rendered == "Hello !"

def test_render_template_with_missing_template_file():
    rendered = render_template(template_input="nonexistent.j2")
    assert rendered == ""

def test_render_template_with_invalid_template_syntax():
    context = {"project_name": "Code Payload"}
    rendered = render_template(template_input="Hello {{ project_name }", **context)
    assert rendered == ""

def test_render_template_with_file_not_found():
    context = {"project_name": "Code Payload"}
    rendered = render_template(template_input="nonexistent_template.j2", **context)
    assert rendered == ""

def test_render_template_with_nonexistent_template():
    context = {"project_name": "Code Payload"}
    rendered = render_template(template_input="nonexistent_template.j2", **context)
    assert rendered == ""  # Should return an empty string if the template file is not found

def test_render_template_with_missing_file():
    context = {"project_name": "Code Payload"}
    rendered = render_template(template_input="nonexistent_template.j2", **context)
    assert rendered == ""  # Should return empty string if template is missing
