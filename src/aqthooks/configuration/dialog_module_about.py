from typing import TYPE_CHECKING

from aqt.qt import (
	Qt, QVBoxLayout, QLabel
)

from .config_dialog_module import ConfigDialogModule
from ...__version__ import VERSION
from ...utils import reloadable_script

if TYPE_CHECKING:
	from .config_dialog import ConfigDialog

# Add the current module to the reloadable modules set
reloadable_script(__name__)


class AboutDialogModule(ConfigDialogModule):
	"""
	About section for the configuration dialog.
	"""

	def __init__(
			self,
			config_dialog: 'ConfigDialog'
	) -> None:
		"""
		Initialize the About dialog module.

		:param config_dialog: The parent configuration dialog.
		"""

		super().__init__(
			name="About",
			config_dialog=config_dialog,
		)

		layout = QVBoxLayout(self)
		layout.setContentsMargins(10, 10, 10, 10)

		# Title label
		lbl_title = QLabel(f"Sky's Jouzu BulkOps")
		lbl_title.setAlignment(Qt.AlignmentFlag.AlignLeft)
		lbl_title.setStyleSheet(
			'font-size: 16pt;'
			'font-weight: bold;'
			'margin-bottom: 0;'
		)

		# Subtitle version
		lbl_version = QLabel(f'v{VERSION}')
		lbl_version.setAlignment(Qt.AlignmentFlag.AlignLeft)
		lbl_version.setStyleSheet(
			'color: gray;'
			'font-size: 10pt;'
			'font-style: italic;'
			'margin-top: 0;'
		)

		# Help label
		lbl_help = QLabel(
			"Welcome to the settings for Sky's Jouzu BulkOps!"
			"<br><br>"
			"Use the menu on the left to select and configure the addon's features. "
			"For more information on a specific option, simply hover your mouse over "
			"its label to view a helpful tooltip."
			"<br><br>"
			"If you encounter any issues or have questions, please report them on the project's "
			"<a href='https://github.com/devExcale/skys-jouzu-bulkops'>GitHub page</a>, "
			"ask in <a href='https://www.youtube.com/@JouzuJuls'>Jouzu Juls</a>'s Discord server, "
			"or send me an <a href='mailto:dev_excale@hotmail.com'>email</a>."
		)
		lbl_help.setWordWrap(True)
		lbl_help.setOpenExternalLinks(True)

		layout.addWidget(lbl_title)
		layout.addWidget(lbl_version)
		layout.addSpacing(10)
		layout.addWidget(lbl_help)
		layout.addStretch()  # Push content to the top

		return
