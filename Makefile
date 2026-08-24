# irakliskyriakidis.eu
#
# make build   render blog/posts/*.md into static HTML
# make run     build, then serve the site at http://localhost:4000
# make stop    stop that server

PYTHON ?= python

.PHONY: help build run stop status deps clean

help:
	@echo "build   - render Markdown posts into HTML"
	@echo "run     - build, then serve at http://localhost:4000"
	@echo "stop    - stop the preview server"
	@echo "status  - is the preview server running?"
	@echo "deps    - install the one Python dependency"
	@echo "clean   - remove generated blog output"

build:
	@$(PYTHON) build.py

run: build
	@$(PYTHON) serve.py start

stop:
	@$(PYTHON) serve.py stop

status:
	@$(PYTHON) serve.py status

deps:
	@$(PYTHON) -m pip install markdown

# Removes generated files only. The Markdown sources in blog/posts are
# untouched, and "make build" puts everything back.
clean:
	@$(PYTHON) -c "import pathlib,shutil; [shutil.rmtree(p) for p in pathlib.Path('blog').iterdir() if p.is_dir() and p.name != 'posts']"
	@echo "removed generated post directories"
