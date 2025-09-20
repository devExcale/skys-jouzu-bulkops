import csv
from io import StringIO
from typing import Dict, Optional

from anki.notes import NoteId
from aqt import mw
from aqt.browser import Browser
from aqt.qt import (
	Qt, QDialog, QVBoxLayout, QTextEdit, QPushButton,
	QLabel, QLayout, QSplitter, QGridLayout, QCheckBox,
	QButtonGroup, QWidget,
)
from aqt.utils import showInfo

from ...utils import get_model_columns

col_note_id = "Note ID"


def aqt_show_csv_io(browser: Browser) -> None:
	"""
	This function will open a modal dialog with two panels: export and import.
	Given the selected notes in the browser,
	the export panel will show a copiable csv export (headers included) of the selected notes.
	The import panel will allow the user to copy a csv (headers included) into the text area,
	and edit the selected notes with the csv data.

	:return:
	"""

	# Create the dialog
	dialog = ModalCSVIO(browser)

	# Show the dialog
	dialog.exec()

	return


class ModalCSVIO(QDialog):
	"""
	This class is used to create a modal dialog with two panels: export and import.
	Given the selected notes in the browser,
	the export panel will show a copiable csv export (headers included) of the selected notes.
	The import panel will allow the user to copy a csv (headers included) into the text area,
	and edit the selected notes with the csv data.
	"""

	def __init__(self, browser: Browser):

		super().__init__(parent=browser)
		self.browser = browser

		self.setWindowTitle("CSV I/O")

		# Layouts
		self.layout: Optional[QLayout] = None
		self.layout_splitter: Optional[QSplitter] = None
		self.layout_export: Optional[QLayout] = None
		self.layout_import: Optional[QLayout] = None
		self.layout_checkboxes: Optional[QLayout] = None
		self.layout_error: Optional[QLayout] = None

		# Labels
		self.lbl_title: Optional[QLabel] = None
		self.lbl_export: Optional[QLabel] = None
		self.lbl_import: Optional[QLabel] = None
		self.lbl_error: Optional[QLabel] = None

		# Buttons
		self.btn_export: Optional[QPushButton] = None
		self.btn_import: Optional[QPushButton] = None

		# TextEdits
		self.edit_export: Optional[QTextEdit] = None
		self.edit_import: Optional[QTextEdit] = None

		models = self.selected_notes_stats()

		if len(models) != 1:
			self.setLayout(self.__layout_error__(models))
			self.setFixedSize(400, 200)
			return

		self.setLayout(self.__layout__(*models.popitem()))

		return

	def __layout__(self, model_name: str, note_count: int) -> QLayout:

		# Create the main layout
		self.layout = QVBoxLayout(self)

		# Title label
		self.lbl_title = QLabel(f'{model_name} - {note_count} notes')

		# Splitter for import/export
		self.layout_splitter = QSplitter()
		self.layout_splitter.setOrientation(Qt.Horizontal)

		# Build the layout
		self.layout.addWidget(self.lbl_title)
		self.layout.addWidget(self.layout_splitter)
		tmp_widget = QWidget()
		tmp_widget.setLayout(self.__layout_export__())
		self.layout_splitter.addWidget(tmp_widget)
		tmp_widget = QWidget()
		tmp_widget.setLayout(self.__layout_import__())
		self.layout_splitter.addWidget(tmp_widget)
		self.layout.addLayout(self.__layout_columns__(model_name))

		return self.layout

	def __layout_export__(self) -> QLayout:

		# Export section
		self.layout_export = QVBoxLayout()

		self.lbl_export = QLabel('Exported CSV (copy this)')

		self.edit_export = QTextEdit()
		self.edit_export.setReadOnly(True)

		self.btn_export = QPushButton('Export')
		self.btn_export.clicked.connect(self.export_csv)

		self.layout_export.addWidget(self.lbl_export)
		self.layout_export.addWidget(self.edit_export)
		self.layout_export.addWidget(self.btn_export)

		return self.layout_export

	def __layout_import__(self) -> QLayout:

		# Export section
		self.layout_import = QVBoxLayout()

		self.lbl_import = QLabel('Paste CSV here to import')

		self.edit_import = QTextEdit()

		self.btn_import = QPushButton('Import')
		self.btn_import.clicked.connect(self.import_csv)

		self.layout_import.addWidget(self.lbl_import)
		self.layout_import.addWidget(self.edit_import)
		self.layout_import.addWidget(self.btn_import)

		return self.layout_import

	def __layout_columns__(self, note_name: str) -> QLayout:

		self.layout_checkboxes = QGridLayout(self)

		self.group_checkboxes = QButtonGroup()
		self.group_checkboxes.setExclusive(False)
		self.group_checkboxes.buttonClicked.connect(self.__on_checkbox_clicked__)

		# Select All checkbox
		self.chk_all = QCheckBox("Select all")
		self.chk_all.setChecked(True)
		self.chk_all.clicked.connect(self.set_all_checkboxes)

		# Note ID checkbox
		self.chk_id = QCheckBox(col_note_id)
		self.chk_id.setChecked(True)
		self.chk_id.setEnabled(False)

		# Add 'Select All'/'Note ID' checkboxes to the layout
		self.layout_checkboxes.addWidget(self.chk_all, 0, 0, 1, 2)
		self.layout_checkboxes.addWidget(self.chk_id, 0, 2, 1, 2)

		# Add other checkboxes
		for i, column in enumerate(get_model_columns(note_name)):
			checkbox = QCheckBox(column)
			checkbox.setChecked(True)
			self.group_checkboxes.addButton(checkbox, i + 1)
			self.layout_checkboxes.addWidget(checkbox, i // 4 + 1, i % 4)

		return self.layout_checkboxes

	def __layout_error__(self, models: Dict[str, int]) -> QLayout:

		self.layout_error = QVBoxLayout(self)

		self.lbl_title = QLabel('Error: a single note type must be selected to perform this operation.')

		str_models = ', '.join(models.keys()) or 'None'

		self.lbl_error.setText(f"Selected note types: {str_models}")
		self.lbl_error.setWordWrap(True)

		self.layout_error.addWidget(self.lbl_title)
		self.layout_error.addWidget(self.lbl_error)

		return self.layout_error

	def set_all_checkboxes(self, state: bool) -> None:

		for btn in self.group_checkboxes.buttons():
			btn.setChecked(state)

		return

	def __on_checkbox_clicked__(self, button: QCheckBox) -> None:
		"""
		This function will be called when a checkbox is clicked.
		It will check if the "Select all" checkbox is checked or not,
		and set the state of all the other checkboxes accordingly.

		:param button: The button that was clicked
		:return:
		"""

		# If all checkboxes are checked, set the 'Select all' checkbox to checked
		state = all(btn.isChecked() for btn in self.group_checkboxes.buttons()) if button.isChecked() else False

		# Update 'Select All' checkbox
		self.chk_all.setChecked(state)

		return

	def selected_notes_stats(self) -> Dict[str, int]:
		"""
		This function will return a dictionary with the names of the selected notes
		and the number of notes of each type.

		:return: The dictionary with the names and counts of the selected notes
		"""

		selected_notes_ids = self.browser.selectedNotes()
		if not selected_notes_ids:
			return dict()

		note_types = dict()
		for note_id in selected_notes_ids:

			note = mw.col.get_note(note_id)
			note_type = note.note_type()["name"]

			if note_type not in note_types:
				note_types[note_type] = 0

			note_types[note_type] += 1

		return note_types

	def export_csv(self):

		selected_notes = self.browser.selectedNotes()
		if not selected_notes:
			self.edit_export.setPlainText("No notes selected.")
			return

		columns = [
			btn.text()
			for btn in self.group_checkboxes.buttons()
			if btn.isChecked()
		]

		output = StringIO()
		writer = csv.writer(output)
		writer.writerow([col_note_id] + columns)

		for note_id in selected_notes:
			note = mw.col.get_note(note_id)
			writer.writerow([note_id] + [note[field] for field in columns])

		self.edit_export.setPlainText(output.getvalue())

		return

	def import_csv(self):

		csv_data = self.edit_import.toPlainText()
		if not csv_data.strip():
			showInfo("No CSV data provided.")
			return

		input_stream = StringIO(csv_data)
		reader = csv.reader(input_stream)
		headers = next(reader, None)

		if not headers or "Note ID" not in headers:
			showInfo("Invalid CSV format. Ensure 'Note ID' is included as the first column.")
			return

		# TODO: check if csv ids are in the selected notes

		note_id_index = headers.index("Note ID")
		for row in reader:
			note_id = NoteId(int(row[note_id_index]))
			note = mw.col.get_note(note_id)
			for i, field in enumerate(headers):
				if field != "Note ID" and field in note:
					note[field] = row[i]
			note.flush()

		mw.col.reset()
		mw.reset()
		showInfo("Notes updated successfully.")

		return
