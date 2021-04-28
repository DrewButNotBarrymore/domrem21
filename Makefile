check_code:
	flake8 .
	isort . --check --diff
	black . -S --check

format_code:
	isort .
	black . -S
