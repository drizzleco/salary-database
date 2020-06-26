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
	pip install -r requirements.txt;

### collect_data - collect disclosure data and save to db
.PHONY: collect_data
collect_data:
	. .env/bin/activate; \
	cat data/salary_links.txt | xargs -n2 -P8 sh -c 'python data/data_to_db.py $$0 $$1'
