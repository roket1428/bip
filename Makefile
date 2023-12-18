.PHONY: venv tests
venv:
	python -m venv --system-site-packages venv

deps: venv
	. ./venv/bin/activate && pip install -r requirements.txt

clean:
	rm -r venv

