from typing import TYPE_CHECKING

from aqt.qt import (
	QVBoxLayout, QFormLayout,
	QLabel, QLineEdit,
)

from .config_dialog_module import ConfigDialogModule
from ..qt_utils import hover_label
from ...utils import reloadable_script

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog

# Add the current module to the reloadable modules set
reloadable_script(__name__)


class UnpackDialogModule(ConfigDialogModule):
	"""
	Configuration dialog module for the dictionary unpack settings.
	"""

	def __init__(
			self,
			config_dialog: 'ConfigDialog'
	) -> None:
		"""
		Initialize the UnpackDialogModule.

		:param config_dialog: The parent configuration dialog.
		"""

		super().__init__(
			name="Dictionary Unpack",
			config_dialog=config_dialog,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(10, 10, 10, 10)

		# Subtitle
		lbl_unpack_subtitle = QLabel('Settings / Dictionary Unpack')
		lbl_unpack_subtitle.setStyleSheet(
			'font-size: 14pt;'
			'font-weight: bold;'
		)

		# Form layout for inputs
		form = QFormLayout()
		form.setContentsMargins(0, 15, 0, 5)

		# 'Dictionary field' input
		lbl_unpack_dictionary_field = hover_label(
			'Dictionary Field',
			'Name of the field where the dictionary output is',
		)
		self.input_unpack_dictionary_field = QLineEdit()

		# 'Reading field' input
		lbl_unpack_reading_field = hover_label(
			'Reading Field',
			'Name of the field where the kana reading should go',
		)
		self.input_unpack_reading_field = QLineEdit()

		# 'Tag fail' input
		lbl_unpack_tag_fail = hover_label(
			'Fail Tag',
			'Name of the tag to apply when the operation fails, leave blank for none',
		)
		self.input_unpack_tag_fail = QLineEdit()

		# Build form layout
		form.addRow(lbl_unpack_dictionary_field, self.input_unpack_dictionary_field)
		form.addRow(lbl_unpack_reading_field, self.input_unpack_reading_field)
		form.addRow(lbl_unpack_tag_fail, self.input_unpack_tag_fail)

		# Build layout
		layout.addWidget(lbl_unpack_subtitle)
		layout.addLayout(form)
		layout.addStretch(1)

		return

	def __on_leave__(self) -> bool:
		"""
		Called when the user navigates away from this module.
		The module can prevent the user from leaving it by returning ``False``.

		:return: ``True`` if the user can leave the module, ``False`` otherwise.
		"""

		# Get settings
		settings = self.config_dialog.settings

		# Edit settings
		settings.unpack.field_dictionary = self.input_unpack_dictionary_field.text().strip()
		settings.unpack.field_reading = self.input_unpack_reading_field.text().strip()
		settings.unpack.tag_fail = self.input_unpack_tag_fail.text().strip()

		return True

	def __sync_settings__(self) -> None:
		"""
		Called when the settings are modified and the ui needs
		to be synced with the settings object.

		:return: ``None``
		"""

		# Get settings
		settings = self.config_dialog.settings

		# Display settings
		self.input_unpack_dictionary_field.setText(settings.unpack.field_dictionary)
		self.input_unpack_reading_field.setText(settings.unpack.field_reading)
		self.input_unpack_tag_fail.setText(settings.unpack.tag_fail)

		return None
