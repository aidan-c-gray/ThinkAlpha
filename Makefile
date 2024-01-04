export IMAGE = thinkalpha

unit-tests: 
	docker build -t $(IMAGE) .
	docker run -it --platform linux/amd64 --rm --env-file secrets.env --entrypoint python $(IMAGE) -m pytest testing/ -vv -p no:cacheprovider
