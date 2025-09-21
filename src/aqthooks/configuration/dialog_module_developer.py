import json
from typing import TYPE_CHECKING

from aqt.qt import (
	Qt, QVBoxLayout, QLabel, QPushButton, QTextEdit,
	QTimer,
)

from .config_dialog_module import ConfigDialogModule
from ...settings import AddonSettings
from ...utils import reloadable_script, log

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
		self.text_edit_json = QTextEdit(self)
		self.text_edit_json.setAcceptRichText(False)

		# Build layout
		layout.addWidget(lbl_title)
		layout.addWidget(lbl_description)
		layout.addWidget(btn_reset, alignment=Qt.AlignmentFlag.AlignLeft)
		layout.addWidget(self.text_edit_json)

		# QTimer for dynamic QTextEdit styling
		self.timer_json_styling = QTimer(self)
		self.timer_json_styling.setSingleShot(True)
		self.timer_json_styling.setInterval(400)

		# Connect signals
		self.text_edit_json.textChanged.connect(self.timer_json_styling.start)
		self.timer_json_styling.timeout.connect(self.perform_json_styling)

		# Style QTextEdit
		self.perform_json_styling()

		return

	def perform_json_styling(self) -> None:

		# Assume json is invalid
		json_valid = False

		try:

			# Parse json and update validity
			json.loads(self.text_edit_json.toPlainText())
			json_valid = True

		except json.JSONDecodeError:
			pass

		# Update stylesheet based on validity
		if json_valid:
			# Reset to default border style
			stylesheet = (
				'font-family: Courier;'
				'font-size: 10pt;'
			)
		else:
			# Custom red border for invalid JSON
			stylesheet = (
				'QTextEdit {'
				'	font-family: Courier;'
				'	font-size: 10pt;'
				'	border: 1px solid red;'
				'}'
				'QTextEdit:focus {'
				'	border: 1px solid salmon;'
				'}'
			)

		# Apply stylesheet
		self.text_edit_json.setStyleSheet(stylesheet)

		return

	def __on_leave__(self) -> bool:
		"""
		Called when the user navigates away from this module.
		The module can prevent the user from leaving it by returning ``False``.

		:return: ``True`` if the user can leave the module, ``False`` otherwise.
		"""

		# Ensure valid JSON
		try:

			config_str = self.text_edit_json.toPlainText()
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
		self.text_edit_json.setPlainText(settings_str)

		return
