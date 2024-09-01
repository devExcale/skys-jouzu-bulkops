# Sky's Jouzu Bulk Operations - Makefile

ADDON_NAME := skys-jouzu-bulkops
ADDON_VERSION := $(shell python __version__.py)
addons21 := $(Anki2)/addons21

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
	cd target/bin && zip -r ../$(ADDON_NAME)-$(ADDON_VERSION).ankiaddon *

install: build
	# Check install location
	@if [ -z "$(Anki2)" ]; then echo "Set Anki2 folder location with 'Anki2' variable."; exit 1; fi

	# Check whether addons21 folder exists
	@if [ ! -d "$(addons21)" ]; then echo "'$(addons21)' folder does not exist."; exit 1; fi

	# Save previous meta.json
	cp $(addons21)/$(ADDON_NAME)/meta.json $(addons21)/$(ADDON_NAME)-meta.json

	# Remove previous installation
	rm -rf $(addons21)/$(ADDON_NAME)

	# Install files
	cp -r target/bin $(addons21)/$(ADDON_NAME)

	# Restore meta.json
	mv $(addons21)/$(ADDON_NAME)-meta.json $(addons21)/$(ADDON_NAME)/meta.json
