from typing import Tuple

from aqt.qt import QLabel, QLineEdit, QFrame, QColor, QWidget, QHBoxLayout


def hover_label(text: str, tooltip: str) -> QLabel:
	"""
	Shortcut to create labels with a given tooltip showed on mouse hover.

	:param text: Label's text
	:param tooltip: Tooltip to apply (html supported)
	:return: The label with the tooltip
	"""

	label = QLabel(text)
	label.setToolTip(tooltip)
	label.setToolTipDuration(-1)

	return label


def input_color_preview(input_placeholder: str) -> Tuple[QWidget, QLineEdit, QFrame]:
	"""
	Creates an input for colors with a small square on the side for color preview.

	:param input_placeholder: Placeholder text for the input field
	:return: A tuple containing the full widget, the input, and the color preview frame
	"""

	# Create input
	line_edit = QLineEdit()
	if input_placeholder:
		line_edit.setPlaceholderText(input_placeholder)

	# Create preview square
	color_preview = QFrame()
	color_preview.setFixedSize(22, 22)
	color_preview.setFrameShape(QFrame.Shape.StyledPanel)
	color_preview.setAutoFillBackground(True)
	__try_preview_color__("white", color_preview)

	# Update preview square on color change
	line_edit.textChanged.connect(
		lambda text, sq=color_preview: __try_preview_color__(text.strip(), sq)
	)

	# Horizontal layout for QLineEdit and QFrame
	input_w_preview = QWidget()
	hbox = QHBoxLayout(input_w_preview)
	hbox.setContentsMargins(0, 0, 0, 0)
	hbox.setSpacing(5)
	hbox.addWidget(line_edit)
	hbox.addWidget(color_preview)

	return input_w_preview, line_edit, color_preview


def __try_preview_color__(text_color: str, widget: QWidget) -> None:
	"""
	Sets the background color on a widget.
	If the color is invalid, the background is set to white with a red border.

	:param text_color: The color to set
	:param widget: The widget to apply the color to
	:return: ``None``
	"""

	qcolor = QColor(text_color)

	if qcolor.isValid():
		style = f'background-color: {text_color}; border: 2px solid #777;'
	else:
		style = 'background-color: white; border: 2px solid red;'

	widget.setStyleSheet(style)

	return
