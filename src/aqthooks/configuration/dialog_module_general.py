from typing import TYPE_CHECKING

from aqt.qt import QVBoxLayout, QCheckBox

from .config_dialog_module import ConfigDialogModule

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog


class GeneralDialogModule(ConfigDialogModule):
	"""
	General settings module for the configuration dialog.
	"""

	def __init__(self, config_dialog: 'ConfigDialog') -> None:
		"""
		Initialize the General dialog module.

		:param config_dialog: The parent configuration dialog.
		"""

		super().__init__(
			name="General",
			config_dialog=config_dialog
		)

		# Create layout
		layout = QVBoxLayout(self)

		# Create checkbox
		self.checkbox_show_changelog = QCheckBox("Show Changelog on Update")

		# Add widgets to layout
		layout.addWidget(self.checkbox_show_changelog)
		layout.addStretch(1)  # Push top

		return

	def __sync_settings__(self) -> None:
		"""
		Called when the settings are modified and the ui needs
		to be synced with the settings object.

		:return: ``None``
		"""

		# Get settings
		settings = self.config_dialog.settings

		# Sync UI with settings
		self.checkbox_show_changelog.setChecked(settings.show_changelog)

		return

	def __on_leave__(self) -> bool:
		"""
		Called when the user navigates away from this module.
		The module can prevent the user from leaving it by returning ``False``.

		:return: ``True`` if the user can leave the module, ``False`` otherwise.
		"""

		# Get settings
		settings = self.config_dialog.settings

		# Update settings
		settings.show_changelog = self.checkbox_show_changelog.isChecked()

		return True
