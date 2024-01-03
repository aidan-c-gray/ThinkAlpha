IMAGE = thinkalpha

unit-tests: 
	docker build -t $(IMAGE) .
	docker run -it --rm --env-file secrets.env --entrypoint python $(IMAGE) -m pytest testing/ -vv -p no:cacheprovider
