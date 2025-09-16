# https://stackoverflow.com/a/78082532
import logging
from pathlib import Path
from typing import Optional

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def get_version() -> Optional[str]:
	try:
		import toml
	except ImportError:
		logging.error("The 'toml' module is not installed. Please install it to retrieve the version.")
		return None

	version = None

	toml_file = Path(__file__).parent / "pyproject.toml"

	if toml_file.exists() and toml_file.is_file():

		data = toml.load(toml_file)

		if "project" in data and "version" in data["project"]:
			version = data["project"]["version"]

	if not version:
		logging.error("Version not found in pyproject.toml.")

	return version


if __name__ == "__main__":
	print(get_version())
