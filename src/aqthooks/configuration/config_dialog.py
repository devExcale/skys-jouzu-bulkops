from typing import Optional, List, Type

from aqt import mw
from aqt.qt import (
	Qt, QDialog, QVBoxLayout, QHBoxLayout, QLayout,
	QLabel, QPushButton, QWidget, QListWidget, QStackedWidget,
)

from .config_dialog_module import ConfigDialogModule
from .dialog_module_about import AboutDialogModule
from .dialog_module_changelog import ChangelogDialogModule
from .dialog_module_developer import DeveloperDialogModule
from .dialog_module_pitch import PitchDialogModule
from .dialog_module_unpack import UnpackDialogModule
from ...settings import AddonSettings
from ...utils import reloadable_script

# Add the current module to the reloadable modules set
reloadable_script(__name__)

# List of configuration modules to include in the dialog
CONFIG_MODULES: List[Type[ConfigDialogModule]] = [
	AboutDialogModule,
	UnpackDialogModule,
	PitchDialogModule,
	ChangelogDialogModule,
	DeveloperDialogModule,
]


class ConfigDialog(QDialog):
	"""
	Configuration dialog for the addon.
	"""

	def __init__(self, parent: Optional[QWidget] = None) -> None:
		"""
		Initialize the configuration dialog.
		:param parent: Parent widget.
		"""

		super().__init__(parent=parent)

		self.setWindowTitle("Settings/Help - Sky's Jouzu BulkOps")
		self.setMinimumSize(450, 400)
		self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

		# Layouts
		self.layout_main: QLayout
		self.layout_panels: QLayout
		self.layout_buttons: QLayout

		# Widgets
		self.list_widget: QListWidget
		self.stacked_widget: QStackedWidget

		# Load modules
		# noinspection PyArgumentList
		self.modules: List[ConfigDialogModule] = [
			module_cls(config_dialog=self) for module_cls in CONFIG_MODULES
		]

		# Build layout and widgets
		self.__build_layout__()

		# Select the first item by default
		if self.list_widget.count() > 0:
			self.list_widget.setCurrentRow(0)

		# Load settings
		self.settings = AddonSettings()
		self.load_settings()

		return

	def __build_layout__(self) -> None:
		"""
		Build the main layout of the dialog and assign it to ``self.layout_main``.
		Sub-layouts are built too by calling their respective methods.

		:return: ``None``
		"""

		self.layout_main = QVBoxLayout(self)

		# Build sub-layouts
		self.__build_layout_panels__()
		self.__build_layout_buttons__()

		self.setLayout(self.layout_main)
		self.layout_main.addLayout(self.layout_panels)
		self.layout_main.addLayout(self.layout_buttons)

		return

	def __build_layout_panels__(self) -> None:
		"""
		Build the main panels layout containing the list of modules on the left
		and assign it to ``self.layout_panels``.

		:return: ``None``
		"""

		self.layout_panels = QHBoxLayout(self)

		# Left panel: List of modules
		self.list_widget = QListWidget(self)
		self.list_widget.setFixedWidth(150)

		# Right panel: Module contents
		self.stacked_widget = QStackedWidget(self)

		# Add modules to the stacked widget
		for module in self.modules:
			self.stacked_widget.addWidget(module)
			self.list_widget.addItem(module.name)

		# Connect the list widget to the stacked widget page
		self.list_widget.currentRowChanged.connect(self.switch_module)

		# Add panels to the layout
		self.layout_panels.addWidget(self.list_widget)
		self.layout_panels.addWidget(self.stacked_widget)

		return

	def __build_layout_buttons__(self) -> None:
		"""
		Build the buttons layout containing Save and Cancel buttons
		and assign it to ``self.layout_buttons``.

		:return: ``None``
		"""

		self.layout_buttons = QHBoxLayout(self)

		lbl_savehint = QLabel('Remember to click Save to apply changes!')
		lbl_savehint.setStyleSheet(
			'color: gray;'
			'font-style: italic;'
		)

		# Save button
		btn_save = QPushButton('Save')
		btn_save.clicked.connect(self.__on_save_clicked__)

		# Cancel button
		btn_cancel = QPushButton('Cancel')
		btn_cancel.clicked.connect(self.reject)

		# Build layout
		self.layout_buttons.addWidget(lbl_savehint)
		self.layout_buttons.addStretch(1)  # Push buttons to the right
		self.layout_buttons.addWidget(btn_save)
		self.layout_buttons.addWidget(btn_cancel)

		return

	def switch_module(self, idx: int) -> None:
		"""
		Switches the current configuration module to the one at the given index.
		The current module is first queried for approval.

		:param idx: Index of the module to switch to.
		:return: ``None``
		"""

		# Skip out of bounds
		if 0 > idx or idx >= self.stacked_widget.count():
			return

		# Skip if current
		if idx == self.stacked_widget.currentIndex():
			return

		# Ask current module if we can leave
		current_module = self.modules[self.stacked_widget.currentIndex()]
		ok = current_module.__on_leave__()

		# If not ok, stay
		if not ok:
			# Change back the list selection
			list_model = self.list_widget.model()
			list_idx = list_model.index(self.stacked_widget.currentIndex(), 0)
			self.list_widget.setCurrentIndex(list_idx)

			return

		# Switch module
		self.stacked_widget.setCurrentIndex(idx)
		new_module = self.modules[idx]
		new_module.__sync_settings__()
		new_module.__on_enter__()

		return

	def load_settings(self) -> None:
		"""
		Load the settings from Anki's configuration and populate the dialog fields.

		:return:
		"""

		# Load settings
		dict_conf = mw.addonManager.getConfig(__name__)
		self.settings = AddonSettings(dict_conf)

		# Update modules' ui
		for module in self.modules:
			module.__sync_settings__()

		return

	def accept_settings(self) -> bool:
		"""
		Accept and save the settings if the current module allows it.

		:return: ``True`` if the settings were accepted and saved, ``False`` otherwise.
		"""

		# Get current index
		idx = self.stacked_widget.currentIndex()

		# Ask current module if we can leave
		ok = self.modules[idx].__on_leave__()

		# If not ok, stay
		if not ok:
			return False

		# Save settings
		mw.addonManager.writeConfig(__name__, self.settings.json())

		return True

	def __on_save_clicked__(self) -> None:
		"""
		Called when the Save button is clicked.
		Attempts to accept and save the settings.
		If successful, closes the dialog.

		:return: ``None``
		"""

		if self.accept_settings():
			self.accept()

		return
