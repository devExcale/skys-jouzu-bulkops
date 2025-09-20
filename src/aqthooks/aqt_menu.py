from typing import Optional

from aqt.browser import Browser
from aqt.qt import QAction

from .actions.actions_csv import aqt_show_csv_io
from .actions.actions_pitch import aqt_colour_from_pitch_selcards
from .actions.actions_unpack import aqt_unpack_reading_selected_cards
from ..utils import log, reload_scripts


def aqt_build_menus(browser: Browser) -> None:
	"""
	Register the actions on the browser menu bar and context menu for the addon operations.

	:param browser: Anki Browser instance
	:return: ``None``
	"""

	# Title
	title_action = QAction("Sky's Jouzu BulkOps", browser)
	title_action.setEnabled(False)

	# Unpack Reading from Meaning
	unpack_action = QAction("Unpack Reading from Meaning", browser)
	unpack_action.triggered.connect(lambda: aqt_unpack_reading_selected_cards(browser))

	# Colour Fields from Pitch Graph
	colour_action = QAction("Colour Fields from Pitch Graph", browser)
	colour_action.triggered.connect(lambda: aqt_colour_from_pitch_selcards(browser))

	# CSV I/O from External CSV
	csv_action = QAction("CSV I/O from External CSV", browser)
	csv_action.triggered.connect(lambda: aqt_show_csv_io(browser))

	# Open Configuration Dialog
	# config_action = QAction("Addon Configuration", browser)
	# config_action.triggered.connect(lambda: open_config_dialog(browser))

	actions = [
		title_action,
		unpack_action,
		colour_action,
		csv_action,
		# config_action,
	]

	# Log actions
	for action in actions:
		log(f"Registering action: {action.text()}")

	# Menu bar
	browser.form.menuEdit.addSeparator()
	for action in actions:
		browser.form.menuEdit.addAction(action)
	browser.form.menuEdit.addSeparator()

	# Context menu
	browser.form.menu_Notes.insertSeparator(browser.form.actionManage_Note_Types)
	for action in actions:
		browser.form.menu_Notes.insertAction(browser.form.actionManage_Note_Types, action)
	browser.form.menu_Notes.insertSeparator(browser.form.actionManage_Note_Types)

	return


def open_config_dialog(browser: Optional[Browser] = None):
	"""Reload the AddonConfigPane source file and open the dialog."""

	# from . import aqt_gui_config
	# from . import qt_utils
	# importlib.reload(aqt_gui_config)
	# importlib.reload(qt_utils)

	# Import "dynamic" modules
	# from . import configuration
	# from .configuration import (
	# 	config_dialog, dialog_module_about, dialog_module_changelog,
	# )
	#
	# # Reload the modules to apply any changes to the code
	# importlib.reload(dialog_module_about)
	# importlib.reload(dialog_module_changelog)
	# importlib.reload(config_dialog)
	# importlib.reload(configuration)

	reload_scripts()

	from .configuration import config_dialog

	dialog = config_dialog.ConfigDialog(parent=browser)

	# Create a new instance of AddonConfigPane
	# dialog = aqt_gui_config.AddonConfigPane(parent=browser)
	dialog.exec()
