### help - help docs for this Makefile
.PHONY: help
help :
	@sed -n '/^###/p' Makefile

### install - install requirements in venv
.PHONY: install
install:
	#  backend installation
	python -m venv .env; \
	. .env/bin/activate; \
	pip install -r requirements.txt;