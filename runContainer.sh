  exec docker run \
 	  --name anaco3 \
          --user=root \
	  --detach=false \
	  -e DISPLAY=${DISPLAY} \
	  -v /tmp/.X11-unix:/tmp/.X11-unix\
	  --rm \
	  -v `pwd`:/mnt/shared \
	  -i \
          -t \
	  yangyang_anaconda3 /bin/bash -c "cd /mnt/shared && python /mnt/shared/play.py"
  exec docker attach anaco3
  exit $