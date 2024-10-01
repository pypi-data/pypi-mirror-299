# code-payload

Condense and summarize a codebase for passing to an LLM as context.

## Features

- **Token-based Summarization**: Summarizes content based on token counts, making it suitable for language models.
- **Flexible Configuration**: Supports configuration through YAML files, environment variables, and CLI arguments.
- **Rich CLI Interface**: Use the CLI to interact with your projects, including rendering Jinja2 templates.
- **Customizable Templates**: Generate custom summaries or reports using Jinja2 templates.

## Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-repo/code-payload.git
cd code-payload
pip install -r requirements.txt
```

## Usage

### Command Line Interface (CLI)

The CLI provides a way to process a project directory and output a summary.

```bash
python src/code_payload/cli.py --help
```

### Example Usage

To process a project directory and output a JSON summary:

```bash
python src/code_payload/cli.py /path/to/your/project
```

To override the file extensions to include:

```bash
python src/code_payload/cli.py /path/to/your/project --include-extensions .py,.js,.md
```

To use a custom template:

```bash
python src/code_payload/cli.py /path/to/your/project --render-args template_input=readme_summary.j2
```

### Configuration

Configuration can be set in a YAML file, through environment variables, or via CLI arguments.

**Example YAML Configuration**:

```yaml
project:
  root: "./"

file_handling:
  max_file_size: 100000
  max_summary_length: 5000
  exclude:
    directories:
      - ".git"
      - "__pycache__"
      - "venv"
      - "env"
      - "node_modules"
    extensions:
      - ".pyc"
      - ".pyo"
      - ".pyd"
      - ".db"
      - ".log"
      - ".sqlite3"
  include:
    extensions:
      - ".py"
      - ".js"
      - ".jsx"
      - ".ts"
      - ".tsx"
      - ".html"
      - ".css"
      - ".json"
      - ".md"

output:
  format: "json"
  file: "output.json"

logging:
  level: "INFO"

tokens:
  max_tokens: 1000
```

### Custom Templates

Two example templates are provided:

- **readme_summary.j2**: Generates a Markdown summary.
- **html_report.j2**: Generates an HTML report.

To use a custom template:

```bash
python src/code_payload/cli.py /path/to/your/project --render-args template_input=html_report.j2
```

### Contributing

Please feel free to fork this repository and submit pull requests.

### License

MIT License.
