# Variables
DOCKER_IMAGE_NAME = my-flask-app
DOCKER_CONTAINER_NAME = my-flask-container
TEST_FILE = upload/word.txt

# Targets
build:
	docker build -t $(DOCKER_IMAGE_NAME) .

run:
	docker run -d -p 5000:5000 --name $(DOCKER_CONTAINER_NAME) $(DOCKER_IMAGE_NAME)

test: build
	docker run  $(DOCKER_IMAGE_NAME) python -u test.py

upload:
	curl -X POST -F "file=@$(TEST_FILE)" http://127.0.0.1:5000/

stop:
	docker stop $(DOCKER_CONTAINER_NAME)
	docker rm $(DOCKER_CONTAINER_NAME)

.PHONY: build run stop test upload
