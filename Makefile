.PHONY: build clean watch

build:
	mdbook build

watch:
	mdbook watch --open

clean:
	rm -rf book
