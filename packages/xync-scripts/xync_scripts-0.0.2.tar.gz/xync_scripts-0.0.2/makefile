PACKAGE := xync_scripts
VENV := venv
VPYTHON := $(VENV)/bin/python

.PHONY: all cv install deps pre-commit clean build twine patch

all: install clean build

cv:
	python3 -m venv venv
install: cv deps pre-commit
	$(VPYTHON) -m pip install -e .[dev]; make pre-commit
deps: $(VENV)
	$(VPYTHON) -m pip install -e .[dev]
pre-commit: .pre-commit-config.yaml
	pre-commit install -t pre-commit -t post-commit -t pre-push

clean: dist $(PACKAGE).egg-info
	rm -rf dist/* $(PACKAGE).egg-info $(PACKAGE)/__pycache__ dist/__pycache__

build:
	$(VPYTHON) -m build; make twine
twine: dist
	$(VPYTHON) -m twine upload dist/* --skip-existing

patch:
	git tag `$(VPYTHON) -m setuptools_scm --strip-dev`; git push --tags --prune -f