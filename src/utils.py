import os
from typing import List

from aqt import mw

ENVKEY_LOG = "SKY_BULKOPS_LOG"


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
