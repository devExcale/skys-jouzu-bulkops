from aqt import mw

from .aqt_gui_config import AddonConfigPane
from .aqt_menu import aqt_build_menus, aqt_refresh_config, open_config_dialog
from ..addon_config import AddonConfig
from ..utils import log


def aqt_init_addon() -> AddonConfig:
	"""
	Init the addon, should be called once when Anki starts.

	:return: Loaded configuration object.
	"""

	log("Registering custom configuration action")

	# Add custom config dialog
	# mw.addonManager.setConfigAction(__name__, lambda: AddonConfigPane().exec())
	mw.addonManager.setConfigAction(__name__, open_config_dialog)

	log("Reloading addon configuration")

	conf = aqt_refresh_config()

	return conf
