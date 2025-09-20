import os
from typing import TYPE_CHECKING

from aqt import mw
from aqt.qt import (
	QVBoxLayout, QTextBrowser
)

from .config_dialog_module import ConfigDialogModule
from ...utils import reloadable_script

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog

# Add the current module to the reloadable modules set
reloadable_script(__name__)


class ChangelogDialogModule(ConfigDialogModule):
	"""
	Dialog module for displaying the changelog.
	"""

	def __init__(
			self,
			config_dialog: 'ConfigDialog'
	) -> None:
		"""
		Initialize the changelog dialog module.

		:param config_dialog: The parent configuration dialog.
		"""

		super().__init__(
			name="Changelog",
			config_dialog=config_dialog,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(10, 0, 10, 0)

		# Text browser for displaying the changelog
		widget_changelog = QTextBrowser(None)
		widget_changelog.setOpenExternalLinks(True)

		try:

			# Compute path to CHANGELOG.md
			addon = mw.addonManager.addonFromModule(__name__)
			path_addon = mw.addonManager.addonsFolder(addon)
			path_changelog = os.path.join(path_addon, "CHANGELOG.md")

			# Read changelog
			with open(path_changelog, 'r', encoding='utf-8') as file:
				content = file.read()

		except OSError:

			content = (
				'# Changelog'
				'\n\n'
				'Changelog file not found.'
			)

		# Display content
		widget_changelog.setMarkdown(content)

		layout.addWidget(widget_changelog)

		return
