.PHONY: help test run server clean

help:
	@echo "MSB v2 make targets:"
	@echo "  make test     - run pytest with project env"
	@echo "  make server   - start uvicorn via start.sh"
	@echo "  make run      - alias for server"
	@echo "  make clean    - remove __pycache__ and .snapshots"

test:
	PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest -q

server:
	./start.sh

run: server

clean:
	rm -rf **/__pycache__ .snapshots
