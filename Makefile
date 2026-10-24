# Project tasks. CI runs format-dry-run, build, test and release.

PACKAGE := uplink

.PHONY: build format format-dry-run test release

build:
	uv sync --locked
	uv run --locked python -m compileall -q $(PACKAGE)

format:
	uv run --locked ruff format .

format-dry-run:
	uv run --locked ruff format --check .

test:
	uv run --locked pytest

release:
	rm -rf dist
	uv build --out-dir dist
