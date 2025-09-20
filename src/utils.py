import importlib
import os
from typing import List

from aqt import mw

ENVKEY_LOG = "SKY_BULKOPS_LOG"

RELOAD_REGISTER = set()


def log(msg: str) -> None:
	"""
	Logs a message to the console if the SKY_BULKOPS_LOG environment variable is set to a non-zero value.

	:param msg: The message to log
	:return: ``None``
	"""

	# Skip log if the environment variable is not set to a non-zero value
	if os.environ.get(ENVKEY_LOG, '0') == '0':
		return

	print(f'[Sky\'s BulkOps/{__name__}] {msg}')

	return


def get_model_columns(model_name: str) -> List[str]:
	"""
	Returns the columns of the given note type, without the note ID column.
	If the note type does not exist, an empty list is returned.

	:return: The columns of the selected note type
	"""

	model = mw.col.models.by_name(model_name)
	if not model:
		return []

	return mw.col.models.fieldNames(model)


def reloadable_script(name: str) -> None:
	"""
	Adds the specified module to the RELOAD_REGISTER set for reloading during development.

	:param name: __name__ of the module to add
	:return: ``None``
	"""

	# TODO: only on debug

	RELOAD_REGISTER.add(name)
	log(f"Marked module for reload: {name}")

	return


def reload_scripts() -> None:
	"""
	Reloads all modules in the RELOAD_REGISTER set.
	This is useful for development purposes, to apply changes without restarting Anki.
	Does a double-pass reload to ensure dependencies are also reloaded.

	:return: ``None``
	"""

	for _ in range(2):
		for module_name in RELOAD_REGISTER:
			module = importlib.import_module(module_name)
			importlib.reload(module)
			log(f"Reloaded module: {module_name}")

	return
