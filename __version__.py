# https://stackoverflow.com/a/78082532

from pathlib import Path
from typing import Optional


def get_version() -> Optional[str]:
	try:
		import toml
	except ImportError:
		return None

	version = None

	toml_file = Path(__file__).parent / "pyproject.toml"

	if toml_file.exists() and toml_file.is_file():

		data = toml.load(toml_file)

		if "project" in data and "version" in data["project"]:
			version = data["project"]["version"]

	return version


if __name__ == "__main__":
	print(get_version())
