from typing import Optional

from aqt import mw
from aqt.qt import (
	Qt, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
	QLabel, QLineEdit, QPushButton, QCheckBox, QWidget,
	QListWidget, QStackedWidget
)

from .qt_utils import hover_label, input_color_preview
from ..__version__ import VERSION
from ..addon_config import AddonConfig


class AddonConfigPane(QDialog):
	"""
	Configuration dialog for addon settings.
	"""

	def __init__(self, parent: Optional[QWidget] = None) -> None:
		super().__init__(parent=parent)
		self.setWindowTitle("Settings/Help - Sky's Jouzu BulkOps")
		self.setMinimumSize(450, 400)

		# Main layout widgets
		self.list_widget: Optional[QListWidget] = None
		self.stacked_widget: Optional[QStackedWidget] = None

		# Set the main layout for the dialog
		self.setLayout(self.__layout__())

		# Load existing configuration
		self.__load_configuration__()

		# Select the first item by default
		if self.list_widget.count() > 0:
			self.list_widget.setCurrentRow(0)

	def __layout__(self) -> QVBoxLayout:
		"""
		Create and return the main layout for the dialog.
		This consists of a vertical layout containing the two-pane horizontal layout
		and the dialog buttons at the bottom.
		"""
		# Top-level layout
		main_layout = QVBoxLayout(self)

		# Two-pane horizontal layout for settings
		paned_layout = QHBoxLayout()

		# Left pane: Category list
		self.list_widget = QListWidget()
		self.list_widget.setFixedWidth(150)

		# Right pane: Stack of configuration pages
		self.stacked_widget = QStackedWidget()

		# Create and add pages to the list and stack
		self.list_widget.addItem("About")
		self.stacked_widget.addWidget(self.__create_page_about__())
		self.list_widget.addItem("Unpack Dictionary")
		self.stacked_widget.addWidget(self.__create_page_unpack__())
		self.list_widget.addItem("Pitch Accent")
		self.stacked_widget.addWidget(self.__create_page_pitch__())

		# Connect list widget to stacked widget
		self.list_widget.currentRowChanged.connect(self.stacked_widget.setCurrentIndex)

		# Add panes to the settings layout
		paned_layout.addWidget(self.list_widget)
		paned_layout.addWidget(self.stacked_widget)

		# Add the main settings layout and the buttons
		main_layout.addLayout(paned_layout)
		main_layout.addLayout(self.__layout_dialog_buttons__())

		return main_layout

	@staticmethod
	def __create_page_about__() -> QWidget:
		"""
		Create and return the widget+layout for the About section.
		"""

		widget_about = QWidget()
		layout_about = QVBoxLayout(widget_about)

		# Title label
		lbl_title = QLabel(f"Sky's Jouzu BulkOps")
		lbl_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
		lbl_title.setStyleSheet(
			'font-size: 16pt;'
			'font-weight: bold;'
			'margin-bottom: 0;'
		)

		# Subtitle version
		lbl_version = QLabel(f'v{VERSION}')
		lbl_version.setAlignment(Qt.AlignmentFlag.AlignLeft)
		lbl_version.setStyleSheet(
			'color: gray;'
			'font-size: 10pt;'
			'font-style: italic;'
			'margin-top: 0;'
		)

		# Help label
		lbl_help = QLabel(
			"Welcome to Sky's Jouzu BulkOps' configuration screen!\n\n"
			'This interface can help you setup the functionalities the addon offers. '
			"You can use the left pane to navigate between each functionality's settings.\n\n"
			'To find out what each option does, you can hover over the labels '
			'and a tooltip will appear with a description.'
		)
		lbl_help.setWordWrap(True)

		layout_about.addWidget(lbl_title)
		layout_about.addWidget(lbl_version)
		layout_about.addSpacing(10)
		layout_about.addWidget(lbl_help)
		layout_about.addStretch()  # Push content to the top

		return widget_about

	def __create_page_unpack__(self) -> QWidget:
		"""
		Create and return the widget+layout for the Unpack section.
		"""

		widget_unpack = QWidget()
		layout_unpack = QVBoxLayout(widget_unpack)
		layout_unpack.setContentsMargins(10, 10, 10, 10)

		# Subtitle
		lbl_unpack_subtitle = QLabel('Settings / Dictionary Unpack')
		lbl_unpack_subtitle.setStyleSheet(
			'font-size: 14pt;'
			'font-weight: bold;'
		)

		# Form layout for inputs
		self.unpack_form_layout = QFormLayout()
		self.unpack_form_layout.setContentsMargins(0, 15, 0, 5)

		# 'Dictionary field' input
		self.lbl_unpack_dictionary_field = hover_label(
			'Dictionary field:',
			'Name of the field where the dictionary output is',
		)
		self.input_unpack_dictionary_field = QLineEdit()

		# 'Reading field' input
		self.lbl_unpack_reading_field = hover_label(
			'Reading field:',
			'Name of the field where the kana reading should go',
		)
		self.input_unpack_reading_field = QLineEdit()

		# 'Tag fail' input
		self.lbl_unpack_tag_fail = hover_label(
			'Tag fail:',
			'Name of the tag to apply when the operation fails, leave blank for none',
		)
		self.input_unpack_tag_fail = QLineEdit()

		# Build form layout
		self.unpack_form_layout.addRow(self.lbl_unpack_dictionary_field, self.input_unpack_dictionary_field)
		self.unpack_form_layout.addRow(self.lbl_unpack_reading_field, self.input_unpack_reading_field)
		self.unpack_form_layout.addRow(self.lbl_unpack_tag_fail, self.input_unpack_tag_fail)

		# Build layout
		layout_unpack.addWidget(lbl_unpack_subtitle)
		layout_unpack.addLayout(self.unpack_form_layout)
		layout_unpack.addStretch(1)

		return widget_unpack

	def __create_page_pitch__(self) -> QWidget:
		"""
		Create and return the widget+layout for the Pitch section.
		"""

		widget_pitch = QWidget()
		layout_pitch = QVBoxLayout(widget_pitch)
		layout_pitch.setContentsMargins(10, 10, 10, 10)

		# Subtitle
		lbl_pitch_subtitle = QLabel('Settings / Pitch Accent')
		lbl_pitch_subtitle.setStyleSheet(
			'font-size: 14pt;'
			'font-weight: bold;'
		)

		# Form layout for inputs
		self.pitch_form_layout = QFormLayout()
		self.pitch_form_layout.setContentsMargins(0, 15, 0, 5)

		# 'Reading field' input
		self.lbl_pitch_reading_field = hover_label(
			'Reading field:',
			'Name of the field where the kana reading and the pitch graph are',
		)
		self.input_pitch_reading_field = QLineEdit()

		# 'Fields to colour' input
		self.lbl_pitch_tocolour_fields = hover_label(
			'Fields to colour:',
			'Comma-separated list of fields to apply the pitch colours to',
		)
		self.input_pitch_tocolour_fields = QLineEdit()

		# Heiban colour input
		self.lbl_pitch_heiban_colour = hover_label(
			'Heiban colour:',
			'Colour for Heiban pitch type<br>e.g., #RRGGBB or a valid color name',
		)
		input_color_preview_heiban, self.input_pitch_heiban_colour, _ = input_color_preview('#RRGGBB or name')

		# Atamadaka colour input
		self.lbl_pitch_atamadaka_colour = hover_label(
			'Atamadaka colour:',
			'Colour for Atamadaka pitch type<br>e.g., #RRGGBB or a valid color name',
		)
		input_color_preview_atamadaka, self.input_pitch_atamadaka_colour, _ = input_color_preview('#RRGGBB or name')

		# Nakadaka colour input
		self.lbl_pitch_nakadaka_colour = hover_label(
			'Nakadaka colour:',
			'Colour for Nakadaka pitch type<br>e.g., #RRGGBB or a valid color name',
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
			'Whether to apply the colour to the pitch graph as well',
		)
		self.chk_pitch_colour_graph = QCheckBox()

		# 'Tag fail' input
		self.lbl_pitch_tag_fail = hover_label(
			'Tag fail:',
			'Name of the tag to apply when the operation fails,<br>leave blank for none',
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
		layout_pitch.addWidget(lbl_pitch_subtitle)
		layout_pitch.addLayout(self.pitch_form_layout)
		layout_pitch.addStretch(1)

		return widget_pitch

	def __layout_dialog_buttons__(self) -> QHBoxLayout:
		"""
		Create and return the dialog buttons.

		:return: A layout containing the dialog's buttons
		"""

		buttons_layout = QHBoxLayout()

		lbl_savehint = QLabel('Remember to click Save to apply changes!')
		lbl_savehint.setStyleSheet(
			'color: gray;'
			'font-style: italic;'
		)

		# Save button
		self.btn_save = QPushButton('Save')
		self.btn_save.clicked.connect(self.__on_save_clicked__)

		# Cancel button
		self.btn_cancel = QPushButton('Cancel')
		self.btn_cancel.clicked.connect(self.reject)

		# Build layout
		buttons_layout.addWidget(lbl_savehint)
		buttons_layout.addStretch(1)  # Push buttons to the right
		buttons_layout.addWidget(self.btn_save)
		buttons_layout.addWidget(self.btn_cancel)

		return buttons_layout

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
		conf.pitch.fields_tocolour = [
			field.strip() for field in self.input_pitch_tocolour_fields.text().split(',') if field.strip()
		]
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
