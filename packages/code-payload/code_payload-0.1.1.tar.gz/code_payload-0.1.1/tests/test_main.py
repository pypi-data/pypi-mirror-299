from omegaconf import OmegaConf

from code_payload.main import main


def test_main_processing(tmp_path):
    (tmp_path / "file1.py").write_text("def foo(): pass")
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
        "tokens": {"max_tokens": 100}
    })
    project_structure = main(config)
    assert project_structure is not None
    assert len(project_structure.files) == 1

def test_main_with_render_false(tmp_path):
    (tmp_path / "file1.py").write_text("def foo(): pass")
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
        "tokens": {"max_tokens": 100}
    })
    project_structure = main(config, render=False)
    assert project_structure is not None
    assert len(project_structure.files) == 1

def test_main_with_invalid_render_args(tmp_path):
    (tmp_path / "file1.py").write_text("def foo(): pass")
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
        "tokens": {"max_tokens": 100}
    })
    render_args = {"template_input": "nonexistent_template.j2"}
    project_structure = main(config, render=True, render_args=render_args)
    assert project_structure is None

def test_main_with_invalid_token_limit(tmp_path):
    (tmp_path / "file1.py").write_text("def foo(): pass")
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
        "tokens": {"max_tokens": 0}  # Invalid token limit
    })
    project_structure = main(config)
    assert project_structure is None  # Expecting None due to invalid config

def test_main_with_empty_project_directory(tmp_path):
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
        "tokens": {"max_tokens": 100}
    })
    project_structure = main(config)
    assert project_structure is not None
    assert len(project_structure.files) == 0

def test_main_without_rendering(tmp_path):
    (tmp_path / "file1.py").write_text("def foo(): pass")
    config = OmegaConf.create({
        "project": {"root": str(tmp_path)},
        "file_handling": {"include": {"extensions": [".py"]}},
        "tokens": {"max_tokens": 100}
    })
    project_structure = main(config, render=False)
    assert project_structure is not None
    assert len(project_structure.files) == 1
