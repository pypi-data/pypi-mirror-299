from typer.testing import CliRunner

from src.code_payload.cli import app

runner = CliRunner()

def test_cli_help():
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output

def test_cli_process(tmp_path):
    # Create a simple directory structure
    (tmp_path / "file1.py").write_text("def foo(): pass")

    # Run the CLI command
    result = runner.invoke(app, [str(tmp_path)])
    assert result.exit_code == 0
    assert "Processing directory" in result.output

def test_cli_with_various_options(tmp_path):
    runner = CliRunner()
    project_path = tmp_path / "example_project"
    project_path.mkdir()
    (project_path / "example.py").write_text("print('Hello World')")

    result = runner.invoke(app, [str(project_path), "--log-level", "DEBUG"])
    assert result.exit_code == 0

    result = runner.invoke(app, [str(project_path), "--include-extensions", ".py,.md"])
    assert result.exit_code == 0

    result = runner.invoke(app, [str(project_path), "--output-file", str(tmp_path / "output.json")])
    assert result.exit_code == 0

def test_cli_with_render_args(tmp_path):
    runner = CliRunner()
    project_path = tmp_path / "example_project"
    project_path.mkdir()
    (project_path / "example.py").write_text("print('Hello World')")

    result = runner.invoke(app, [str(project_path), "--render-args", "template_input=readme_summary.j2"])
    assert result.exit_code == 0
    assert "Processing directory" in result.output

def test_cli_with_missing_output_file(tmp_path):
    runner = CliRunner()
    project_path = tmp_path / "example_project"
    project_path.mkdir()
    (project_path / "example.py").write_text("print('Hello World')")

    result = runner.invoke(app, [str(project_path), "--output-file", "nonexistent/output.json"])
    assert result.exit_code == 0
    assert "Processing directory" in result.output

def test_cli_with_logging_levels(tmp_path):
    runner = CliRunner()
    project_path = tmp_path / "example_project"
    project_path.mkdir()
    (project_path / "example.py").write_text("print('Hello World')")

    # Test different logging levels
    result = runner.invoke(app, [str(project_path), "--log-level", "DEBUG"])
    assert result.exit_code == 0

    result = runner.invoke(app, [str(project_path), "--log-level", "ERROR"])
    assert result.exit_code == 0

def test_cli_with_invalid_render_args(tmp_path):
    runner = CliRunner()
    project_path = tmp_path / "example_project"
    project_path.mkdir()
    (project_path / "example.py").write_text("print('Hello World')")

    # Test with invalid render args
    result = runner.invoke(app, [str(project_path), "--render-args", "invalid_arg"])
    assert result.exit_code != 0  # Expecting failure due to invalid args

    # Test with missing output file option
    result = runner.invoke(app, [str(project_path), "--output-file", ""])
    assert result.exit_code != 0  # Expecting failure due to missing output file

def test_cli_with_specific_config_and_output_file(tmp_path):
    runner = CliRunner()
    config_file = tmp_path / "config.yaml"
    config_file.write_text("project:\n  root: './'")

    output_file = tmp_path / "output.json"
    project_path = tmp_path / "example_project"
    project_path.mkdir()
    (project_path / "example.py").write_text("print('Hello World')")

    result = runner.invoke(app, [
        str(project_path),
        "--config-file", str(config_file),
        "--output-file", str(output_file),
        "--log-level", "INFO"
    ])
    assert result.exit_code == 0
    assert output_file.exists()
