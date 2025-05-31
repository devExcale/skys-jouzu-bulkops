from typing import List

from aqt import mw


def log(msg):
	print(f"[{__name__}] {msg}")


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
