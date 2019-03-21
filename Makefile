sphinx: litprog html

html:
	sphinx-build -b html -E . _build/

litprog:
	sphinx-build -b litprog -E . _build/

testpypi: sphinx test _confirm
	rm -rf dist
	rm -rf *.egg-info
	./setup.py sdist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi: sphinx test _confirm
	rm -rf dist
	rm -rf *.egg-info
	./setup.py sdist
	twine upload dist/*

# See https://stackoverflow.com/a/47839479/857390
_confirm:
	@(read -p "Are you sure? [y/N]: " sure && \
	  case "$$sure" in [yY]) true;; *) false;; esac )

test:
	pytest

