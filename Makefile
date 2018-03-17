# Execute with
# make start
#
# If you want more than 3 containers started
# execute with CONTAINER_COUNT env set

NAME := alexconrey/pymemcached-server
CONTAINER_COUNT ?= 3

NUMBERS := $(shell seq 1 ${CONTAINER_COUNT})
CONTAINERS := $(addprefix server,${NUMBERS})

.PHONY: build run info start stop 
build:
	docker build --rm -t $(NAME) .

run: build
	$(foreach ctname,$(CONTAINERS),docker run -d -t --name=$(ctname) $(NAME); )

info: 
	$(foreach ctname,$(CONTAINERS),docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(ctname);)

lint:
	pylint memcrashed.py --function-naming-style=snake_case --const-naming-style=snake_case

test: lint

start: build run info

stop:
	$(foreach ctname,$(CONTAINERS),docker rm -f $(ctname);)

default: start
