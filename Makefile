REBUILD_FLAG =

.PHONY: all
all: venv test

.PHONY: venv
venv: .venv.touch
	tox2 -e venv $(REBUILD_FLAG)

.PHONY: tests test
tests: test
test: .venv.touch
	tox2 --skip-missing-interpreters $(REBUILD_FLAG)

.venv.touch: setup.py requirements-dev.txt
	$(eval REBUILD_FLAG := --recreate)
	touch .venv.touch

.PHONY: clean
clean:
	find . -iname '*.pyc' | xargs rm -f
	rm -rf .tox
	rm -rf ./venv-*
	rm -f .venv.touch
