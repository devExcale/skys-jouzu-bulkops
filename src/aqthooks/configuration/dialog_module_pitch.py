from typing import TYPE_CHECKING

from aqt.qt import (
	QVBoxLayout, QFormLayout,
	QLabel, QLineEdit, QGroupBox, QCheckBox,
)

from .config_dialog_module import ConfigDialogModule
from ..qt_utils import hover_label, input_color_preview
from ...utils import reloadable_script

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog

# Add the current module to the reloadable modules set
reloadable_script(__name__)


class PitchDialogModule(ConfigDialogModule):
	"""
	Configuration dialog module for pitch accent settings.
	"""

	def __init__(
			self,
			config_dialog: 'ConfigDialog'
	) -> None:
		"""
		Initialize the pitch accent configuration dialog module.

		:param config_dialog: The parent configuration dialog.
		"""

		super().__init__(
			name="Pitch Accent",
			config_dialog=config_dialog,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(10, 10, 10, 10)

		# Subtitle
		lbl_pitch_subtitle = QLabel('Settings / Pitch Accent')
		lbl_pitch_subtitle.setStyleSheet(
			'font-size: 14pt;'
			'font-weight: bold;'
		)

		# Form layout for inputs
		form = QFormLayout()
		form.setContentsMargins(0, 15, 0, 5)

		# Group boxes
		group_colors = QGroupBox('Colours')
		form_colors = QFormLayout(group_colors)

		# 'Reading field' input
		lbl_pitch_reading_field = hover_label(
			'Reading Field',
			'Name of the field where the kana reading and the pitch graph are',
		)
		self.input_pitch_reading_field = QLineEdit()

		# 'Fields to colour' input
		lbl_pitch_tocolour_fields = hover_label(
			'Fields To Colour',
			'Comma-separated list of fields to apply the pitch colours to',
		)
		self.input_pitch_tocolour_fields = QLineEdit()

		# Heiban colour input
		lbl_pitch_heiban_colour = hover_label(
			"Heiban <font color='gray'>[LHH.H]</font>",
			'Colour for Heiban pitch type<br>e.g., #RRGGBB or a valid color name',
		)
		input_color_preview_heiban, self.input_pitch_heiban_colour, _ = input_color_preview('#RRGGBB or name')

		# Atamadaka colour input
		lbl_pitch_atamadaka_colour = hover_label(
			"Atamadaka <font color='gray'>[HLL.L]</font>",
			'Colour for Atamadaka pitch type<br>e.g., #RRGGBB or a valid color name',
		)
		input_color_preview_atamadaka, self.input_pitch_atamadaka_colour, _ = input_color_preview('#RRGGBB or name')

		# Nakadaka colour input
		lbl_pitch_nakadaka_colour = hover_label(
			"Nakadaka <font color='gray'>[LHL.L]</font>",
			'Colour for Nakadaka pitch type<br>e.g., #RRGGBB or a valid color name',
		)
		input_color_preview_nakadaka, self.input_pitch_nakadaka_colour, _ = input_color_preview('#RRGGBB or name')

		# Oodaka colour input
		lbl_pitch_oodaka_colour = hover_label(
			"Oodaka <font color='gray'>[LHH.L]</font>",
			'Colour for Oodaka pitch type<br>e.g., #RRGGBB or a valid color name'
		)
		input_color_preview_oodaka, self.input_pitch_oodaka_colour, _ = input_color_preview('#RRGGBB or name')

		# 'Colour graph' checkbox
		lbl_pitch_colour_graph = hover_label(
			'Colour Graph',
			'Whether to apply the colour to the pitch graph as well',
		)
		self.chk_pitch_colour_graph = QCheckBox()

		# 'Tag fail' input
		lbl_pitch_tag_fail = hover_label(
			'Fail Tag',
			'Name of the tag to apply when the operation fails,<br>leave blank for none',
		)
		self.input_pitch_tag_fail = QLineEdit()

		# Build form layout
		form_colors.addRow(lbl_pitch_heiban_colour, input_color_preview_heiban)
		form_colors.addRow(lbl_pitch_atamadaka_colour, input_color_preview_atamadaka)
		form_colors.addRow(lbl_pitch_nakadaka_colour, input_color_preview_nakadaka)
		form_colors.addRow(lbl_pitch_oodaka_colour, input_color_preview_oodaka)

		form.addRow(lbl_pitch_reading_field, self.input_pitch_reading_field)
		form.addRow(lbl_pitch_tocolour_fields, self.input_pitch_tocolour_fields)
		form.addRow(group_colors)
		form.addRow(lbl_pitch_colour_graph, self.chk_pitch_colour_graph)
		form.addRow(lbl_pitch_tag_fail, self.input_pitch_tag_fail)

		# Build layout
		layout.addWidget(lbl_pitch_subtitle)
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
		settings.pitch.field_reading = self.input_pitch_reading_field.text().strip()
		settings.pitch.fields_tocolour = [
			field.strip() for field in self.input_pitch_tocolour_fields.text().split(',') if field.strip()
		]
		settings.pitch.colour_heiban = self.input_pitch_heiban_colour.text().strip()
		settings.pitch.colour_atamadaka = self.input_pitch_atamadaka_colour.text().strip()
		settings.pitch.colour_nakadaka = self.input_pitch_nakadaka_colour.text().strip()
		settings.pitch.colour_oodaka = self.input_pitch_oodaka_colour.text().strip()
		settings.pitch.colour_graph = self.chk_pitch_colour_graph.isChecked()
		settings.pitch.tag_fail = self.input_pitch_tag_fail.text().strip()

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
		self.input_pitch_reading_field.setText(settings.pitch.field_reading)
		self.input_pitch_tocolour_fields.setText(', '.join(settings.pitch.fields_tocolour))
		self.input_pitch_heiban_colour.setText(settings.pitch.colour_heiban)
		self.input_pitch_atamadaka_colour.setText(settings.pitch.colour_atamadaka)
		self.input_pitch_nakadaka_colour.setText(settings.pitch.colour_nakadaka)
		self.input_pitch_oodaka_colour.setText(settings.pitch.colour_oodaka)
		self.chk_pitch_colour_graph.setChecked(settings.pitch.colour_graph)
		self.input_pitch_tag_fail.setText(settings.pitch.tag_fail)

		return None
