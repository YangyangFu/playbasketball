IMA_NAME = yangyang_anaconda3

COMMAND_RUN = docker run \
	  --name anaco3 \
	  --detach=false \
	  -e DISPLAY=${DISPLAY} \
	  -v /tmp/.X11-unix:/tmp/.X11-unix \
	  --rm \
	  -v `pwd`:/mnt/shared \
	  -i \
          -t \
	  ${IMG_NAME} /bin/bash -c

build:
	docker build --no-cache --rm -t ${IMA_NAME} .

remove_image:
	docker rmi ${IMA_NAME}

Run:
	${COMMAND_RUN} \
		"cd /mnt/shared && bash"