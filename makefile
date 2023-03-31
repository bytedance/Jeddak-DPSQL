
lint:
	@flake8 --statistics

test:
	PYTHONPATH=. pytest -n 4 -sv tests/unit_test --durations=0

fast_test:
	pytest -sv tests/unit_test -k "not all_analysisbase" 

cov:
	PYTHONPATH=. pytest --cov=. --cov-report=html tests/unit_test

TIME := $(shell date "+%G%m%d_%H%M%S")