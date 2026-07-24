.PHONY: help test verify run server clean worktree-agent worktree-merge

help:
	@echo "MSB v2 make targets:"
	@echo "  make test       - run pytest with project env"
	@echo "  make verify     - pytest + ruff (+optional bandit)"
	@echo "  make server     - start uvicorn via start.sh"
	@echo "  make run        - alias for server"
	@echo "  make clean      - remove __pycache__ and .snapshots"
	@echo "  make worktree-agent TASK='...' - isolate an agent checkout"
	@echo "  make worktree-merge BRANCH=... [BASE=main] - merge agent worktree"

verify:
	@echo "Running verification gate..."
	PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest -q --tb=short
	ruff check .
	@echo "Verification gate passed."

test:
	PYTHONPATH=/Users/lordwilson/msb-v2 MSB_REASONING_SCORER=1 /opt/homebrew/Caskroom/miniforge/base/bin/python -m pytest -q
	PYTHONPATH=/Users/lordwilson/msb-v2 /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/assert_contract_coverage.py
	PYTHONPATH=/Users/lordwilson/msb-v2 /opt/homebrew/Caskroom/miniforge/base/bin/python scripts/verify_anonymous_routes.py

server:
	./start.sh

run: server

clean:
	rm -rf **/__pycache__ .snapshots

worktree-agent:
	@if [ -z "$(TASK)" ]; then echo "Usage: make worktree-agent TASK='description'"; exit 1; fi
	bash .hermes/scripts/worktree-agent.sh "$(TASK)"

worktree-merge:
	@if [ -z "$(BRANCH)" ]; then echo "Usage: make worktree-merge BRANCH=agent/... [BASE=main]"; exit 1; fi
	bash .hermes/scripts/worktree-merge.sh "$(BRANCH)" "$(BASE)"
