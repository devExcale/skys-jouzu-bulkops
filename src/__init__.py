from aqt import gui_hooks
from aqt.browser import Browser
from aqt.qt import QAction

from .addon_config import AddonConfig
from .colour_pitch import colour_fields
from .unpack_reading import unpack_reading_in_cards


def setup_browser_menu(browser: Browser):
	# Title
	title_action = QAction("Sky's Jouzu BulkOps", browser)
	title_action.setEnabled(False)

	# Unpack Reading from Meaning
	unpack_action = QAction("Unpack Reading from Meaning", browser)
	unpack_action.triggered.connect(lambda: unpack_reading_in_cards(browser))

	# Colour Fields from Pitch Graph
	colour_action = QAction("Colour Fields from Pitch Graph", browser)
	colour_action.triggered.connect(lambda: colour_fields(browser))

	# Menu bar
	browser.form.menuEdit.addSeparator()
	browser.form.menuEdit.addAction(title_action)
	browser.form.menuEdit.addAction(unpack_action)
	browser.form.menuEdit.addAction(colour_action)
	browser.form.menuEdit.addSeparator()

	# Context menu
	browser.form.menu_Notes.insertSeparator(browser.form.actionManage_Note_Types)
	browser.form.menu_Notes.insertAction(
		browser.form.actionManage_Note_Types, title_action
	)
	browser.form.menu_Notes.insertAction(
		browser.form.actionManage_Note_Types, unpack_action
	)
	browser.form.menu_Notes.insertAction(
		browser.form.actionManage_Note_Types, colour_action
	)
	browser.form.menu_Notes.insertSeparator(browser.form.actionManage_Note_Types)


gui_hooks.browser_menus_did_init.append(setup_browser_menu)

# Reload config
AddonConfig()
