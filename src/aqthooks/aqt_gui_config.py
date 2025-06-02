from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
	QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
	QLabel, QLineEdit, QPushButton, QCheckBox, QWidget
)
from aqt import mw

from .qt_utils import hover_label, input_color_preview
from ..addon_config import AddonConfig


class AddonConfigPane(QDialog):
	"""
	Configuration dialog for addon settings.
	"""

	def __init__(self, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent=parent)

		self.setWindowTitle('Sky\'s Jouzu BulkOps - Settings')

		# Layouts
		self.main_layout: Optional[QVBoxLayout] = None
		self.unpack_form_layout: Optional[QFormLayout] = None
		self.pitch_form_layout: Optional[QFormLayout] = None
		self.buttons_layout: Optional[QHBoxLayout] = None

		# Main Title
		self.lbl_title: Optional[QLabel] = None
		self.lbl_help: Optional[QLabel] = None

		# --- [Unpack] Section ---
		self.lbl_unpack_subtitle: Optional[QLabel] = None

		# Labels for Unpack config
		self.lbl_unpack_dictionary_field: Optional[QLabel] = None
		self.lbl_unpack_reading_field: Optional[QLabel] = None
		self.lbl_unpack_tag_fail: Optional[QLabel] = None

		# Inputs for Unpack config
		self.input_unpack_dictionary_field: Optional[QLineEdit] = None
		self.input_unpack_reading_field: Optional[QLineEdit] = None
		self.input_unpack_tag_fail: Optional[QLineEdit] = None

		# --- [Pitch] Section ---
		self.lbl_pitch_subtitle: Optional[QLabel] = None

		# Labels for Pitch config
		self.lbl_pitch_reading_field: Optional[QLabel] = None
		self.lbl_pitch_tocolour_fields: Optional[QLabel] = None
		self.lbl_pitch_heiban_colour: Optional[QLabel] = None
		self.lbl_pitch_atamadaka_colour: Optional[QLabel] = None
		self.lbl_pitch_nakadaka_colour: Optional[QLabel] = None
		self.lbl_pitch_oodaka_colour: Optional[QLabel] = None
		self.lbl_pitch_colour_graph: Optional[QLabel] = None
		self.lbl_pitch_tag_fail: Optional[QLabel] = None

		# Inputs for Pitch config
		self.input_pitch_reading_field: Optional[QLineEdit] = None
		self.input_pitch_tocolour_fields: Optional[QLineEdit] = None
		self.input_pitch_heiban_colour: Optional[QLineEdit] = None
		self.input_pitch_atamadaka_colour: Optional[QLineEdit] = None
		self.input_pitch_nakadaka_colour: Optional[QLineEdit] = None
		self.input_pitch_oodaka_colour: Optional[QLineEdit] = None
		self.chk_pitch_colour_graph: Optional[QCheckBox] = None
		self.input_pitch_tag_fail: Optional[QLineEdit] = None

		# Dialog buttons
		self.btn_save: Optional[QPushButton] = None
		self.btn_cancel: Optional[QPushButton] = None

		# Set the main layout for the dialog
		self.setLayout(self.__layout__())

		# Load existing configuration
		self.__load_configuration__()

		# Adjust dialog size to fit contents
		self.adjustSize()

		return

	def __layout__(self) -> QVBoxLayout:
		"""
		Create and return the layout for the whole dialog.
		"""

		self.main_layout = QVBoxLayout(self)

		# Title label
		self.lbl_title = QLabel('Configuration')
		self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
		font_title = self.lbl_title.font()
		font_title.setPointSize(16)
		font_title.setBold(True)
		self.lbl_title.setFont(font_title)

		# Help label
		self.lbl_help = QLabel(
			'Welcome to the Addon Configuration!\n'
			'This interface can help you setup the functionalities this addon offers.\n\n'
			'To find out what each option does, you can hover over the labels '
			'and a tooltip will appear with a description.'
		)

		# Build layout
		self.main_layout.addWidget(self.lbl_title)
		self.main_layout.addSpacing(10)
		self.main_layout.addWidget(self.lbl_help)
		self.main_layout.addSpacing(10)
		self.main_layout.addLayout(self.__layout_unpack__())
		self.main_layout.addSpacing(15)
		self.main_layout.addLayout(self.__layout_pitch__())
		self.main_layout.addStretch(1)  # Push buttons to the bottom
		self.main_layout.addLayout(self.__layout_dialog_buttons__())

		return self.main_layout

	def __layout_unpack__(self) -> QVBoxLayout:
		"""
		Create and return the layout for the Unpack section.
		"""

		layout_unpack = QVBoxLayout()

		# Subtitle
		self.lbl_unpack_subtitle = QLabel('-- Unpack --')
		font_subtitle = self.lbl_unpack_subtitle.font()
		font_subtitle.setBold(True)
		font_subtitle.setPointSize(12)
		self.lbl_unpack_subtitle.setFont(font_subtitle)

		# Form layout for inputs
		self.unpack_form_layout = QFormLayout()
		self.unpack_form_layout.setContentsMargins(20, 5, 0, 5)

		# 'Dictionary field' input
		self.lbl_unpack_dictionary_field = hover_label(
			'Dictionary field:',
			'Name of the field where the dictionary output is'
		)
		self.input_unpack_dictionary_field = QLineEdit()

		# 'Reading field' input
		self.lbl_unpack_reading_field = hover_label(
			'Reading field:',
			'Name of the field where the kana reading should go'
		)
		self.input_unpack_reading_field = QLineEdit()

		# 'Tag fail' input
		self.lbl_unpack_tag_fail = hover_label(
			'Tag fail:',
			'Name of the tag to apply when the operation fails, leave blank for none'
		)
		self.input_unpack_tag_fail = QLineEdit()

		# Build form layout
		self.unpack_form_layout.addRow(self.lbl_unpack_dictionary_field, self.input_unpack_dictionary_field)
		self.unpack_form_layout.addRow(self.lbl_unpack_reading_field, self.input_unpack_reading_field)
		self.unpack_form_layout.addRow(self.lbl_unpack_tag_fail, self.input_unpack_tag_fail)

		# Build layout
		layout_unpack.addWidget(self.lbl_unpack_subtitle)
		layout_unpack.addLayout(self.unpack_form_layout)

		return layout_unpack

	def __layout_pitch__(self) -> QVBoxLayout:
		"""
		Create and return the layout for the Pitch section.
		"""

		layout_pitch = QVBoxLayout()

		# Subtitle
		self.lbl_pitch_subtitle = QLabel('-- Pitch --')
		font_subtitle = self.lbl_pitch_subtitle.font()
		font_subtitle.setBold(True)
		font_subtitle.setPointSize(12)
		self.lbl_pitch_subtitle.setFont(font_subtitle)

		# Form layout for inputs
		self.pitch_form_layout = QFormLayout()
		self.pitch_form_layout.setContentsMargins(20, 5, 0, 5)

		# 'Reading field' input
		self.lbl_pitch_reading_field = hover_label(
			'Reading field:',
			'Name of the field where the kana reading and the pitch graph are'
		)
		self.input_pitch_reading_field = QLineEdit()

		# 'Fields to colour' input
		self.lbl_pitch_tocolour_fields = hover_label(
			'Fields to colour:',
			'Comma-separated list of fields to apply the pitch colours to'
		)
		self.input_pitch_tocolour_fields = QLineEdit()

		# Heiban colour input
		self.lbl_pitch_heiban_colour = hover_label(
			'Heiban colour:',
			'Colour for Heiban pitch type<br>e.g., #RRGGBB or a valid color name'
		)
		input_color_preview_heiban, self.input_pitch_heiban_colour, _ = input_color_preview('#RRGGBB or name')

		# Atamadaka colour input
		self.lbl_pitch_atamadaka_colour = hover_label(
			'Atamadaka colour:',
			'Colour for Atamadaka pitch type<br>e.g., #RRGGBB or a valid color name'
		)
		input_color_preview_atamadaka, self.input_pitch_atamadaka_colour, _ = input_color_preview('#RRGGBB or name')

		# Nakadaka colour input
		self.lbl_pitch_nakadaka_colour = hover_label(
			'Nakadaka colour:',
			'Colour for Nakadaka pitch type<br>e.g., #RRGGBB or a valid color name'
		)
		input_color_preview_nakadaka, self.input_pitch_nakadaka_colour, _ = input_color_preview('#RRGGBB or name')

		# Oodaka colour input
		self.lbl_pitch_oodaka_colour = hover_label(
			'Oodaka colour:',
			'Colour for Oodaka pitch type<br>e.g., #RRGGBB or a valid color name'
		)
		input_color_preview_oodaka, self.input_pitch_oodaka_colour, _ = input_color_preview('#RRGGBB or name')

		# 'Colour graph' checkbox
		self.lbl_pitch_colour_graph = hover_label(
			'Colour graph:',
			'Whether to apply the colour to the pitch graph as well'
		)
		self.chk_pitch_colour_graph = QCheckBox()

		# 'Tag fail' input
		self.lbl_pitch_tag_fail = hover_label(
			'Tag fail:',
			'Name of the tag to apply when the operation fails,<br>leave blank for none'
		)
		self.input_pitch_tag_fail = QLineEdit()

		# Build form layout
		self.pitch_form_layout.addRow(self.lbl_pitch_reading_field, self.input_pitch_reading_field)
		self.pitch_form_layout.addRow(self.lbl_pitch_tocolour_fields, self.input_pitch_tocolour_fields)
		self.pitch_form_layout.addRow(self.lbl_pitch_heiban_colour, input_color_preview_heiban)
		self.pitch_form_layout.addRow(self.lbl_pitch_atamadaka_colour, input_color_preview_atamadaka)
		self.pitch_form_layout.addRow(self.lbl_pitch_nakadaka_colour, input_color_preview_nakadaka)
		self.pitch_form_layout.addRow(self.lbl_pitch_oodaka_colour, input_color_preview_oodaka)
		self.pitch_form_layout.addRow(self.lbl_pitch_colour_graph, self.chk_pitch_colour_graph)
		self.pitch_form_layout.addRow(self.lbl_pitch_tag_fail, self.input_pitch_tag_fail)

		# Build layout
		layout_pitch.addWidget(self.lbl_pitch_subtitle)
		layout_pitch.addLayout(self.pitch_form_layout)
		return layout_pitch

	# Placeholder: User might want more sophisticated validation or error handling.

	def __layout_dialog_buttons__(self) -> QHBoxLayout:
		"""
		Create and return the dialog buttons.

		:return: A layout containing the dialog's buttons
		"""

		self.buttons_layout = QHBoxLayout()

		# Save button
		self.btn_save = QPushButton('Save')
		self.btn_save.clicked.connect(self.__on_save_clicked__)

		# Cancel button
		self.btn_cancel = QPushButton('Cancel')
		self.btn_cancel.clicked.connect(self.reject)

		# Build layout
		self.buttons_layout.addStretch(1)  # Push buttons to the right
		self.buttons_layout.addWidget(self.btn_save)
		self.buttons_layout.addWidget(self.btn_cancel)

		return self.buttons_layout

	def __load_configuration__(self) -> None:
		"""
		Load existing configuration values into the input fields.
		"""

		dict_conf = mw.addonManager.getConfig(__name__)
		conf = AddonConfig(dict_conf)

		# Unpack section
		self.input_unpack_dictionary_field.setText(conf.unpack.field_dictionary)
		self.input_unpack_reading_field.setText(conf.unpack.field_reading)
		self.input_unpack_tag_fail.setText(conf.unpack.tag_fail)

		# Pitch section
		self.input_pitch_reading_field.setText(conf.pitch.field_reading)
		self.input_pitch_tocolour_fields.setText(', '.join(conf.pitch.fields_tocolour))
		self.input_pitch_heiban_colour.setText(conf.pitch.colour_heiban)
		self.input_pitch_atamadaka_colour.setText(conf.pitch.colour_atamadaka)
		self.input_pitch_nakadaka_colour.setText(conf.pitch.colour_nakadaka)
		self.input_pitch_oodaka_colour.setText(conf.pitch.colour_oodaka)
		self.chk_pitch_colour_graph.setChecked(conf.pitch.colour_graph)
		self.input_pitch_tag_fail.setText(conf.pitch.tag_fail)

		return

	def __on_save_clicked__(self):
		"""
		Save the configuration settings from the input fields.
		"""

		# Blank configuration
		conf = AddonConfig()

		# Unpack section
		conf.unpack.field_dictionary = self.input_unpack_dictionary_field.text().strip()
		conf.unpack.field_reading = self.input_unpack_reading_field.text().strip()
		conf.unpack.tag_fail = self.input_unpack_tag_fail.text().strip()

		# Pitch section
		conf.pitch.field_reading = self.input_pitch_reading_field.text().strip()
		conf.pitch.fields_tocolour = list(map(str.strip, self.input_pitch_tocolour_fields.text().split(',')))
		conf.pitch.colour_heiban = self.input_pitch_heiban_colour.text().strip()
		conf.pitch.colour_atamadaka = self.input_pitch_atamadaka_colour.text().strip()
		conf.pitch.colour_nakadaka = self.input_pitch_nakadaka_colour.text().strip()
		conf.pitch.colour_oodaka = self.input_pitch_oodaka_colour.text().strip()
		conf.pitch.colour_graph = self.chk_pitch_colour_graph.isChecked()
		conf.pitch.tag_fail = self.input_pitch_tag_fail.text().strip()

		# Save config
		mw.addonManager.writeConfig(__name__, conf.json())

		self.accept()

		return
