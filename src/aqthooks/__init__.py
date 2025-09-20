from aqt import mw

from .aqt_menu import aqt_build_menus, open_config_dialog
from ..utils import log


def aqt_init_addon() -> None:
	"""
	Init the addon, should be called once when Anki starts.

	:return: Loaded configuration object.
	"""

	log("Registering custom configuration action")

	# Add custom config dialog
	mw.addonManager.setConfigAction(__name__, open_config_dialog)

	return
