import re
from enum import Enum
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

re_pitch_section = re.compile(r'<!-- (?:user_)?accent_start -->(.*?)<!-- (?:user_)?accent_end -->')
""" Regex for extracting the pitch graph section """

re_tags_pitch_svg = re.compile(r'</?(?:svg|circle).*?>')
""" Regex to find all svg/circle tags """

re_tag_start_font_color = re.compile(r'^<font color=".*?">(.*)$')
""" Regex to find font tag with colour """

re_svg_graph_text = re.compile(r'<text(.*?)fill:.*?;(.*?)>')
""" Regex to find text in the svg graph """

re_svg_graph_path = re.compile(r'<path(.*?)stroke:.*?;(.*?)>')
""" Regex to find paths in the svg graph """

re_svg_graph_circle = re.compile(r'<circle r="5"(.*?)fill:.*?;(.*?)>')
""" Regex to find circles (rad. 5) in the svg graph """


class PitchTypes(Enum):
	HEIBAN = "heiban"
	ATAMADAKA = "atamadaka"
	NAKADAKA = "nakadaka"
	OODAKA = "oodaka"


def infer_pitch_type_from_graph(svg_root: Element) -> Optional[PitchTypes]:
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


def find_pitch_graph_xml(field_content: str) -> Optional[Element]:
	"""
	Find the root of the accent svg in the field content.

	:param field_content: string containing the field content
	:return: root of the accent svg or None if not found
	"""
	match = re_pitch_section.search(field_content)
	if not match:
		return None

	# Find all tags returned in a list, then join them
	accent_tags = re_tags_pitch_svg.findall(match.group(1))
	accent_tags = "".join(accent_tags)

	# Return the accent tags as an Element
	return ElementTree.fromstring(accent_tags)


def apply_colour_to_field(text: str, colour: str, colour_graph: bool = False) -> str:
	"""
	Apply a colour to the text and optionally to the pitch graph.
	This function assumes there is at most one pitch graph in the text.

	:param text: text to colour
	:param colour: colour to apply
	:param colour_graph: whether to apply the colour to the pitch graph
	:return: coloured text
	"""

	# Split text by pitch graph
	match_pitch = re_pitch_section.search(text)
	if match_pitch:
		pitch_section = match_pitch.group(0)
		texts = text.split(pitch_section)
	else:
		pitch_section = ''
		texts = [text]

	# Apply colour to each part of the text
	for i, subtext in enumerate(texts):

		# Skip empty subtexts
		if not subtext:
			continue

		# Find color tag in subtext
		match_font = re_tag_start_font_color.match(subtext)

		if match_font:
			# Replace color in tag
			subtext = f'<font color="{colour}">{match_font.group(1)}'
		else:
			# Wrap text in color
			subtext = f'<font color="{colour}">{subtext}</font>'

		texts[i] = subtext

	# Colour the pitch graph
	if pitch_section and colour_graph:
		def repl_colour_text(match: re.Match):
			""" Replace all colours in svg text tags """
			return f'<text{match.group(1)}fill:{colour} !important;{match.group(2)}>'

		def repl_colour_path(match: re.Match):
			""" Replace all colours in svg path tags """
			return f'<path{match.group(1)}stroke:{colour} !important;{match.group(2)}>'

		def repl_colour_circle(match: re.Match):
			""" Replace all colours in svg circle tags (with rad. 5) """
			return f'<circle r="5"{match.group(1)}fill:{colour} !important;{match.group(2)}>'

		pitch_section = re_svg_graph_text.sub(repl_colour_text, pitch_section)
		pitch_section = re_svg_graph_path.sub(repl_colour_path, pitch_section)
		pitch_section = re_svg_graph_circle.sub(repl_colour_circle, pitch_section)

	# Join the text parts and the pitch section
	return texts[0] + pitch_section + (''.join(texts[1:]) if len(texts) > 1 else '')
