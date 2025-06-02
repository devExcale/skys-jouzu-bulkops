from aqt.browser import Browser

from .aqt_menu import aqt_build_menus, aqt_refresh_config
from ..addon_config import AddonConfig


def aqt_init_addon(browser: Browser) -> AddonConfig:
	aqt_build_menus(browser)
	conf = aqt_refresh_config()

	return conf
