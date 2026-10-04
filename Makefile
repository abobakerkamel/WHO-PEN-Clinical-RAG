.PHONY: test secret-scan validate

test:
	pytest -q

secret-scan:
	python scripts/secret_scan.py .

validate:
	python scripts/validate_notebook.py
	python scripts/secret_scan.py .
	pytest -q
