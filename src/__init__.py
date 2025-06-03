import os

try:
	from aqt import mw, gui_hooks
	from .aqthooks import aqt_init_addon, aqt_build_menus

	gui_hooks.main_window_did_init.append(aqt_init_addon)
	gui_hooks.browser_menus_did_init.append(aqt_build_menus)
except ImportError as e:

	if os.environ.get("SKY_BULKOPS_SKIP_AQT", "0") != "1":
		raise e

	print("[Sky's Jouzu BulkOps] Running in testing mode, skipping aqt initialization")
