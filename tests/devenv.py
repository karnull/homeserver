from pathlib import Path

from uplink.config import Config
from uplink.projects import slugify


def make_project(
    config: Config, name: str, compose: bool = True, root: Path | None = None
) -> Path:
    """A project laid out the way devenv init leaves it: the folder, and its compose files in envs_dir."""
    path = (root or config.projects_dir) / name
    (path / "main").mkdir(parents=True)
    env_dir = make_env(config, slugify(name), project_root=path)
    if not compose:
        (env_dir / "compose.yaml").unlink()
    return path


def make_env(config: Config, slug: str, project_root: Path) -> Path:
    env_dir = config.envs_dir / slug
    env_dir.mkdir(parents=True, exist_ok=True)
    (env_dir / "compose.yaml").write_text("services: {}\n")
    (env_dir / ".env").write_text(f"PROJECT_SLUG={slug}\nPROJECT_ROOT={project_root}\n")
    return env_dir
