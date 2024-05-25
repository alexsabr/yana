SHELL = /usr/bin/bash
init: .venv


clean: 
	rm -r .venv


.venv:
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	python3 -m pip install -r requirements.txt

dock:
	docker build -f ./docker/Dockerfile  .
