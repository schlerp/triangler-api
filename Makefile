# this is our root dir, this makefile must stay at the root of the repo
ROOT_DIR:=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))

APP_NAME:="triangler_api"

.PHONY:
	run-develop run-prod

run-develop:
	docker build --target develop -t ${APP_NAME} . && docker run --rm --env-file ./dev.env -v ${ROOT_DIR}/src/triangle_api:/app -p 8000:8000 ${APP_NAME}

run-shell:
	docker build --target develop -t ${APP_NAME} . && docker run --rm -it --env-file ./dev.env -v ${ROOT_DIR}/src/triangle_api:/app --entrypoint bash -p 8000:8000 ${APP_NAME}

run-prod:
	docker build --target prod -t ${APP_NAME} . && docker run --rm --env-file ./prod.env -p 8000:8000 ${APP_NAME}
