import re
from enum import Enum
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

# Regex for extracting the accent section
re_accent = re.compile(r"<!-- (?:user_)?accent_start -->(.*)<!-- (?:user_)?accent_end -->")
# Regex to check whether there's an accent section at the end
re_accent_ends = re.compile(r"<!-- (?:user_)?accent_start -->.*?<!-- (?:user_)?accent_end -->$")
# Regex to find all svg/circle tags
re_tags = re.compile(r"</?(?:svg|circle).*?>")
# Regex to find global font tag with colour
re_font_color_start = re.compile(r"^<font color=\".*?\">(.*)$")


class PitchTypes(Enum):
	HEIBAN = "heiban"
	ATAMADAKA = "atamadaka"
	NAKADAKA = "nakadaka"
	OODAKA = "oodaka"


def infer_pitch_type(svg_root: Element) -> Optional[PitchTypes]:
	"""
	Infer the pitch type from the accent svg root.

	:param svg_root: root of the accent svg
	:return: pitch type or None if not found
	"""

	# Get all y values on distinct x values
	# (assuming if x values overlap then y values are the same)
	nodes = {
		int(node.attrib["cx"]): int(node.attrib["cy"])
		for node
		in svg_root
	}

	# Order on x values and get y values
	y_values = list(map(lambda t: t[1], sorted(nodes.items())))

	if len(y_values) < 2:
		return None

	# Get highest y value (svg axis is inverted, from top to bottom)
	y_high = min(y_values)

	# First node high: atamadaka
	if y_values[0] == y_high:
		return PitchTypes.ATAMADAKA

	# First node low, other nodes high: heiban
	if all(map(lambda y: y == y_high, y_values[1:])):
		return PitchTypes.HEIBAN

	# First node low, other nodes high except last: oodaka
	if all(map(lambda y: y == y_high, y_values[1:-1])):
		return PitchTypes.OODAKA

	# Other cases: nakadaka
	return PitchTypes.NAKADAKA


def find_accent_svg_root(field_content: str) -> Optional[Element]:
	"""
	Find the root of the accent svg in the field content.

	:param field_content: string containing the field content
	:return: root of the accent svg or None if not found
	"""
	match = re_accent.search(field_content)
	if not match:
		return None

	# Find all tags returned in a list, then join them
	accent_tags = re_tags.findall(match.group(1))
	accent_tags = "".join(accent_tags)

	# Return the accent tags as an Element
	return ElementTree.fromstring(accent_tags)


def apply_colour(text: str, colour: str) -> str:
	"""
	Apply a colour to the text.

	:param text: text to colour
	:param colour: colour to apply
	:return: coloured text
	"""

	# Check whether there's a font tag wrapping the text
	match = re_font_color_start.match(text)

	if match:
		# Change the colour on the font tag
		return f"<font color=\"{colour}\">{match.group(1)}"

	# Save accent sections
	ending_accent = re_accent_ends.findall(text)

	# Remove ending accent if found
	if ending_accent:
		text = text.replace(ending_accent[0], "")

	# Apply the colour
	text = f"<font color=\"{colour}\">{text}</font>"

	# Re-apply the accent section
	if ending_accent:
		text += ending_accent[0]

	return text
