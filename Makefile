.PHONY: setup test lint status fetch-latest

setup:            ## create .venv and install everything (needs uv)
	UV_LINK_MODE=copy uv sync --extra ui

test:             ## run the test suite
	.venv/bin/pytest -q

lint:             ## ruff check
	.venv/bin/ruff check vazante tests

status:           ## environment report
	.venv/bin/vazante status

fetch-latest:     ## one informe month + dictionary + cad_fi into data/raw (smoke test of the bulk layer)
	.venv/bin/vazante cvm fetch --months 1 && .venv/bin/vazante cvm meta && .venv/bin/vazante cvm cad-fi
