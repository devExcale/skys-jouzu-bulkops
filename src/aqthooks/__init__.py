from aqt import mw
from aqt.browser import Browser

from .aqt_gui_config import AddonConfigPane
from .aqt_menu import aqt_build_menus, aqt_refresh_config
from ..addon_config import AddonConfig


def aqt_init_addon(browser: Browser) -> AddonConfig:
	aqt_build_menus(browser)

	# Add custom config dialog
	mw.addonManager.setConfigAction(__name__, lambda: AddonConfigPane().exec())

	conf = aqt_refresh_config()

	return conf
