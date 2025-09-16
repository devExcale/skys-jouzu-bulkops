# Sky's Jouzu Bulk Operations - Makefile

ADDON_NAME := skys-jouzu-bulkops
ADDON_VERSION := $(shell python __version__.py)
addons21 := $(Anki2)/addons21

# Print commands only on verbose
ifndef VERBOSE
	MAKEFLAGS += --silent
endif

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

	# Print release version
	echo "VERSION = '$(ADDON_VERSION)'" > target/bin/__version__.py

	# Create the .ankiaddon file
	cd target/bin && zip -r ../$(ADDON_NAME)-$(ADDON_VERSION).ankiaddon * -x __pycache__/*

install: build
	# Check install location
	if [ -z "$(Anki2)" ]; \
		then echo "Set Anki2 folder location with 'Anki2' variable."; \
		exit 1; \
	fi

	# Check whether addons21 folder exists
	if [ ! -d "$(addons21)" ]; \
		then echo "'$(addons21)' folder does not exist."; \
		exit 1; \
	fi

	# Save previous meta.json (if present)
	if [ -f $(addons21)/$(ADDON_NAME)/meta.json ]; then \
		cp $(addons21)/$(ADDON_NAME)/meta.json $(addons21)/$(ADDON_NAME)-meta.json; \
	fi

	# Remove previous installation
	rm -rf $(addons21)/$(ADDON_NAME)

	# Install files
	cp -r target/bin $(addons21)/$(ADDON_NAME)

	# Restore meta.json (if previously present)
	if [ -f $(addons21)/$(ADDON_NAME)-meta.json ]; then \
		mv $(addons21)/$(ADDON_NAME)-meta.json $(addons21)/$(ADDON_NAME)/meta.json; \
	fi
