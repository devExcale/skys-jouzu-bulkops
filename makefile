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

install: build
	# Check install location
	@if [ -z "$(Anki2)" ]; then echo "Set Anki2 folder location with 'Anki2' variable."; exit 1; fi

	# Check whether addons21 folder exists
	@if [ ! -d "$(Anki2)/addons21" ]; then echo "'$(Anki2)/addons21' folder does not exist."; exit 1; fi

	# Remove previous installation
	rm -rf $(Anki2)/addons21/skys-jouzu-bulkops

	# Install files
	cp -r target/bin $(Anki2)/addons21/skys-jouzu-bulkops
