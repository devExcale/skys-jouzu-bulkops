import re
from enum import Enum
from types import SimpleNamespace
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from aqt import mw
from aqt.browser import Browser
from aqt.utils import showInfo

from .addon_config import AddonConfig

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


def colour_fields(browser: Browser) -> None:
	"""
	Colour the fields based on the pitch graph.

	:param browser: browser object
	"""

	conf = AddonConfig().pitch
	field_read = conf.field_reading
	fields_tocolour = set(conf.fields_tocolour)
	colours = {
		PitchTypes.HEIBAN: conf.colour_heiban,
		PitchTypes.ATAMADAKA: conf.colour_atamadaka,
		PitchTypes.NAKADAKA: conf.colour_nakadaka,
		PitchTypes.OODAKA: conf.colour_oodaka,
	}

	# Operation counts
	counts = SimpleNamespace(
		total=0,
		edited=0,
		no_graph=0,
		no_fields=0,
	)

	# Iterate over selected notes
	for note_id in browser.selectedNotes():

		# Increase total count
		counts.total += 1

		# Get note
		note = mw.col.get_note(note_id)

		# noinspection PyBroadException
		try:

			# Find input field
			if not (field_read in note):
				counts.no_fields += 1
				raise Exception("No reading field")

			# Find output fields
			if not (fields_tocolour.issubset(note.keys())):
				counts.no_fields += 1
				raise Exception("Not all output fields found")

			# Find root of accent svg
			svg_root = find_accent_svg_root(note[field_read])
			if svg_root is None:
				counts.no_graph += 1
				raise Exception("No graph found")

			# Find pitch type
			pitch_type = infer_pitch_type(svg_root)
			if pitch_type is None:
				counts.no_graph += 1
				raise Exception("No graph found")

			colour = colours[pitch_type]

			# Apply colour to the fields
			for field in fields_tocolour:

				# Skip empty fields
				text = note[field]
				if not text:
					continue

				note[field] = apply_colour(text, colour)

			# Increase edited count
			counts.edited += 1

		except Exception:

			# Add fail tag to note
			note.add_tag(conf.tag_fail)

		finally:

			# Update the note
			note.flush()

	# Reset the collection and the main window
	mw.col.reset()
	mw.reset()

	# Final info message
	info_msg = (
		'「終わった」 (*￣▽￣)b\n\n'
		'Edited {edited} notes out of {total} selected\n'
		'Notes without graph: {no_graph}\n'
		'Notes without fields: {no_fields}'
	).format(**counts.__dict__)

	if counts.edited < counts.total:
		info_msg += "\n\nTip: did you set the correct fields in the config?"

	showInfo(info_msg, title="Bulk Colouring Results")


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
