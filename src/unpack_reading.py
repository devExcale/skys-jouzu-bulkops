import re
from types import SimpleNamespace
from typing import Tuple

from aqt import mw
from aqt.browser import Browser
from aqt.utils import showInfo

from .addon_config import AddonConfig

# Regex for extracting the reading (hiragana) this format: e.g. "たる【足る】 ★★★★"
re_reading = re.compile(r"(.*).*【.*】.*")


def unpack_reading_in_cards(browser: Browser):
	"""

	:return:
	"""

	conf = AddonConfig().unpack
	field_dict = conf.field_dictionary
	field_read = conf.field_reading

	# Operation counts
	counts = SimpleNamespace(
		total=0,
		edited=0,
		no_reading=0,
		no_fields=0,
	)

	# Iterate over selected notes
	for note_id in browser.selectedNotes():

		# Increase total count
		counts.total += 1

		# Get note
		note = mw.col.get_note(note_id)

		# Find i/o fields
		if not (field_dict in note and field_read in note):
			counts.no_fields += 1
			continue

		# Unpack the fields
		reading, meaning = unpack_reading(note[field_dict])

		# Check if no reading
		if reading == "":
			counts.no_reading += 1
			continue

		# Update the fields
		note[field_read] = reading
		note[field_dict] = meaning

		# Increase edited count
		counts.edited += 1

		# Update the note
		note.flush()

	# Reset the collection and the main window
	mw.col.reset()
	mw.reset()

	# Final info message
	info_msg = (
		'「終わった」 (*￣▽￣)b\n\n'
		'Edited Notes: {edited}/{total}\n'
		'Notes w/out reading: {no_reading}\n'
		'Notes w/out fields: {no_fields}'
	).format(**counts.__dict__)

	showInfo(info_msg, title="Reading Unpacking Results")


def unpack_reading(content: str) -> Tuple[str, str]:
	"""
	Unpack the content of a field into reading and meaning.
	If the content cannot be parsed, an empty string is returned for the reading and the meaning is returned as is;
	otherwise, the reading and the meaning (minus the reading) are returned.

	:param content: The content of the field
	:return: A tuple containing the reading and meaning
	"""

	# Split on newline
	split = content.split("<br>")

	# First line contains reading
	reading = split[0]

	# Extract the reading
	match = re_reading.search(reading)
	if match:
		reading = match.group(1)
	else:
		return "", content

	# The rest is the meaning
	meaning = '<br>'.join(split[1:])

	return reading, meaning
