from typing import TYPE_CHECKING

from aqt.qt import QWidget

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog


# noinspection PyMethodMayBeStatic

class ConfigDialogModule(QWidget):
	"""
	Base class for configuration dialog modules.
	"""

	def __init__(
			self,
			name: str,
			config_dialog: 'ConfigDialog',
	) -> None:
		"""
		Initialize the configuration dialog module.

		:param name: The name of the module.
		:param config_dialog: The parent configuration dialog.
		"""
		super().__init__(parent=config_dialog)

		self.config_dialog: ConfigDialog = config_dialog
		self.name: str = name

		return

	def __on_enter__(self) -> None:
		"""
		Called when the user navigates to this module.

		:return: ``None``
		"""

		return None

	def __on_leave__(self) -> bool:
		"""
		Called when the user navigates away from this module.
		The module can prevent the user from leaving it by returning ``False``.

		:return: ``True`` if the user can leave the module, ``False`` otherwise.
		"""

		return True

	def __sync_settings__(self) -> None:
		"""
		Called when the settings are modified and the ui needs
		to be synced with the settings object.

		:return: ``None``
		"""

		return None
