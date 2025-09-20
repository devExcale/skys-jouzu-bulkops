import re
from types import SimpleNamespace

from aqt import mw
from aqt.browser import Browser
from aqt.utils import showInfo

from ...pitch import find_pitch_graph_xml, infer_pitch_type_from_graph, apply_colour_to_field, PitchTypes
from ...settings import AddonSettings

# Regex for extracting the accent section
re_accent = re.compile(r"<!-- (?:user_)?accent_start -->(.*)<!-- (?:user_)?accent_end -->")

# Regex to check whether there's an accent section at the end
re_accent_ends = re.compile(r"<!-- (?:user_)?accent_start -->.*?<!-- (?:user_)?accent_end -->$")

# Regex to find all svg/circle tags
re_tags = re.compile(r"</?(?:svg|circle).*?>")

# Regex to find global font tag with colour
re_font_color_start = re.compile(r"^<font color=\".*?\">(.*)$")


def aqt_colour_from_pitch_selcards(browser: Browser) -> None:
	"""
	Colour the fields based on the pitch graph.

	:param browser: browser object
	"""

	key_conf = mw.addonManager.getConfig(__name__)
	conf = AddonSettings(key_conf).pitch

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

	# Start undo checkpoint
	undo_id = mw.col.add_custom_undo_entry("Bulk Colour from Pitch Graph")

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
			svg_root = find_pitch_graph_xml(note[field_read])
			if svg_root is None:
				counts.no_graph += 1
				raise Exception("No graph found")

			# Find pitch type
			pitch_type = infer_pitch_type_from_graph(svg_root)
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

				note[field] = apply_colour_to_field(text, colour, colour_graph=conf.colour_graph)

			# Increase edited count
			counts.edited += 1

		except Exception:

			# Add fail tag to note
			if conf.tag_fail:
				note.add_tag(conf.tag_fail)

		finally:

			# Update the note
			mw.col.update_note(note)

	# End undo checkpoint
	mw.col.merge_undo_entries(undo_id)

	# Reset the collection and the main window
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

	return
