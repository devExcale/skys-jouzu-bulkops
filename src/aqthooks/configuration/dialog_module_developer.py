import json
from typing import TYPE_CHECKING

from aqt.qt import (
	Qt, QVBoxLayout, QLabel, QPushButton, QTextEdit
)

from .config_dialog_module import ConfigDialogModule
from ...settings import AddonSettings
from ...utils import reloadable_script

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog

# Add the current module to the reloadable modules set
reloadable_script(__name__)


class DeveloperDialogModule(ConfigDialogModule):
	"""
	Configuration dialog module for raw JSON configuration editing.
	"""

	def __init__(
			self,
			config_dialog: 'ConfigDialog'
	) -> None:
		"""
		Initialize the developer configuration dialog module.

		:param config_dialog: The parent configuration dialog.
		"""

		super().__init__(
			name="Developer Configuration",
			config_dialog=config_dialog,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(10, 10, 10, 0)

		# Title
		lbl_title = QLabel('Raw Configuration')
		lbl_title.setStyleSheet(
			'font-size: 14pt;'
			'font-weight: bold;'
		)

		# Description
		lbl_description = QLabel(
			'Here you can view and edit the raw JSON configuration for the addon.'
			'\n'
			'Edit this only if you know what you are doing! '
			'Use the reset button down below to restore the previous values.'
		)

		# Reset button
		btn_reset = QPushButton('Reset')
		btn_reset.setToolTip('Reset the configuration to the previous values')
		btn_reset.clicked.connect(self.__sync_settings__)

		# Text area for JSON configuration
		self.text_edit_raw_config = QTextEdit(self)
		self.text_edit_raw_config.setAcceptRichText(False)
		self.text_edit_raw_config.setStyleSheet(
			'font-family: Courier;'
			'font-size: 10pt;'
		)

		# Build layout
		layout.addWidget(lbl_title)
		layout.addWidget(lbl_description)
		layout.addWidget(btn_reset, alignment=Qt.AlignmentFlag.AlignLeft)
		layout.addWidget(self.text_edit_raw_config)

		return

	def __on_leave__(self) -> bool:
		"""
		Called when the user navigates away from this module.
		The module can prevent the user from leaving it by returning ``False``.

		:return: ``True`` if the user can leave the module, ``False`` otherwise.
		"""

		# Ensure valid JSON
		try:

			config_str = self.text_edit_raw_config.toPlainText()
			dict_conf = json.loads(config_str)

		except json.JSONDecodeError:
			return False

		# Save configuration
		self.config_dialog.settings = AddonSettings(dict_conf)

		return True

	def __sync_settings__(self) -> None:
		"""
		Called when the settings are modified and the ui needs
		to be synced with the settings object.

		:return: ``None``
		"""

		# Get current settings
		dict_conf = self.config_dialog.settings.json()

		# Pretty print JSON
		settings_str = json.dumps(dict_conf, indent=4)
		self.text_edit_raw_config.setPlainText(settings_str)

		return
