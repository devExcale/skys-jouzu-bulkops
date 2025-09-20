from aqt import mw

from .aqt_menu import aqt_build_menus, open_config_dialog
from .configuration.config_dialog import ConfigDialog
from .configuration.dialog_module_changelog import ChangelogDialogModule
from ..__version__ import VERSION
from ..settings import AddonSettings
from ..utils import log


def aqt_init_addon() -> None:
	"""
	Init the addon, should be called once when Anki starts.

	:return: Loaded configuration object.
	"""

	log("Registering custom configuration action")

	# Add custom config dialog
	mw.addonManager.setConfigAction(__name__, open_config_dialog)

	prompt_changelog_on_update()

	return


def prompt_changelog_on_update() -> None:
	"""
	Prompt the user with the changelog if the addon was updated
	and the user has enabled the option to show the changelog on update.

	:return: ``None``
	"""

	# Load settings
	dict_conf = mw.addonManager.getConfig(__name__)
	settings = AddonSettings(dict_conf)

	# Check version change
	if settings.version == VERSION:
		return

	# Set new version and save
	settings.version = VERSION
	mw.addonManager.writeConfig(__name__, settings.json())

	# Check whether to show the changelog
	if not settings.show_changelog:
		return

	# Load and show changelog dialog
	dialog = ConfigDialog(parent=mw)
	dialog.set_module(ChangelogDialogModule)
	dialog.exec()

	return
