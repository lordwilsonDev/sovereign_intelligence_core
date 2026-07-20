.PHONY: help test run server clean

help:
	@echo "MSB v2 make targets:"
	@echo "  make test     - run pytest with project env"
	@echo "  make server   - start uvicorn via start.sh"
	@echo "  make run      - alias for server"
	@echo "  make clean    - remove __pycache__ and .snapshots"

test:
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest -q
	PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONPATH=/Users/lordwilson/msb-v2 /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/assert_contract_coverage.py

server:
	./start.sh

run: server

clean:
	rm -rf **/__pycache__ .snapshots
