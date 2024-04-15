lint:
	poetry run black .
	poetry run isort .
	poetry run ruff check .
	poetry run mypy .


gen_requirement:
	poetry export -f requirements.txt --output requirements/requirements.txt

	
gen_dev_requirement:
	poetry export -f requirements.txt --output requirements/dev-requirements.txt --with dev,test


get_data_set:
	kaggle competitions download -c home-credit-default-risk
	mkdir -p .cache/data
	unzip home-credit-default-risk.zip -d .cache/data/
	rm home-credit-default-risk.zip
