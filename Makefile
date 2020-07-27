### help - help docs for this Makefile
.PHONY: help
help :
	@sed -n '/^###/p' Makefile

### install - install requirements in venv
.PHONY: install
install:
	#  backend installation
	python3 -m venv .env; \
	. .env/bin/activate; \
	pip install -r requirements.txt \
	pip install -e . &&\
	python manage.py db upgrade;

### collect_2019_data - collect disclosure data for 2019 and save to db
.PHONY: collect_2019_data
collect_2019_data:
	. .env/bin/activate; \
	cat data/salary_links.txt | xargs -n2 sh -c 'python data/data_to_db.py $$0 $$1'

### lint - lint code
.PHONY: lint
lint:
	isort -rc --multi-line=3 --trailing-comma --force-grid-wrap=0 --use-parentheses --line-width=88 backend/
	black backend

### clean - delete data and database files
.PHONY: clean
clean:
	rm data/*.sqlite data/*.csv data/*.xlsx
