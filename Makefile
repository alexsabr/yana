SHELL = /usr/bin/bash
init: .venv

clean:
	rm -r .venv


.venv:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install -r requirements.txt && \
	python3 -m spacy download fr_core_news_sm 


dock:
	docker build --tag yana    --progress=plain -f ./docker/Dockerfile  .


run-compose:
	docker compose  -f ./docker/compose.yml up --force-recreate --remove-orphans


stop-compose:
	docker compose -f ./docker/compose.yml down


run-alone:
	docker run --rm  -p 8080:80 yana:latest
