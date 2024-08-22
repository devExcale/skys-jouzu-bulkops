# Read version from file
VERSION := $(shell python __version__.py)

all: build

# Remove every output file
clean:
	# Remove the target directory
	rm -rf target

# Create the .ankiaddon file
build:
	# Remove previous build
	rm -rf target/bin

	# Create target directory
	mkdir -p target/bin

	# Copy files to target
	cp -r src/* target/bin
	cp -r resources/* target/bin

	# Create the .ankiaddon file
	cd target/bin && zip -r ../skys-jouzu-bulkops-$(VERSION).ankiaddon *

