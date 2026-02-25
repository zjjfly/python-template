# init uv
uv venv --python 3.12
uv python pin 3.12
# install tools
uv tool install ruff
uv tool install mypy
uv tool install pre-commit
uv sync
