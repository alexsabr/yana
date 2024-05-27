SHELL = /usr/bin/bash
init: .venv


clean:
	rm -r .venv


.venv:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install -r requirements.txt

dock:
	docker build --no-cache --tag yana    --progress=plain -f ./docker/Dockerfile  .

run-compose:
	docker compose up  --force-recreate --file docker/compose.yml

run-alone:
	docker run --rm  -p 8080:80 yana:latest
