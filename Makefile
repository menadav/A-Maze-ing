VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip

run: $(VENV)
	$(PYTHON) a-maze-ing.py config.txt

$(VENV): requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install ./maze_app/generator

lint: $(VENV)
	$(VENV)/bin/flake8 a-maze-ing.py parse maze_app
	$(VENV)/bin/mypy a-maze-ing.py parse maze_app \
		--explicit-package-bases \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
clean:
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

.PHONY: run lint clean
