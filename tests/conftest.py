import pytest
from fastapi.testclient import TestClient

from uplink.app import create_app
from uplink.config import Config


@pytest.fixture
def config(tmp_path):
    projects = tmp_path / "Projects"
    projects.mkdir()
    return Config(
        projects_dir=projects,
        socket_path=tmp_path / "uplink.sock",
        token_file=tmp_path / "token",
        audit_log=tmp_path / "audit.log",
    )


@pytest.fixture
def client(config):
    return TestClient(create_app(config))
