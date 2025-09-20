from types import SimpleNamespace

from aqt import mw
from aqt.browser import Browser
from aqt.utils import showInfo

from ..settings import AddonSettings
from ..unpack import unpack_reading


def aqt_unpack_reading_selected_cards(browser: Browser):
	"""

	:return:
	"""

	dict_conf = mw.addonManager.getConfig(__name__)
	conf = AddonSettings(dict_conf).unpack

	field_dict = conf.field_dictionary
	field_read = conf.field_reading

	# Operation counts
	counts = SimpleNamespace(
		total=0,
		edited=0,
		no_reading=0,
		no_fields=0,
	)

	# Start undo checkpoint
	undo_id = mw.col.add_custom_undo_entry("Bulk Unpack Dictionary")

	# Iterate over selected notes
	for note_id in browser.selectedNotes():

		# Increase total count
		counts.total += 1

		# Get note
		note = mw.col.get_note(note_id)

		# noinspection PyBroadException
		try:

			# Find i/o fields
			if not (field_dict in note and field_read in note):
				counts.no_fields += 1
				raise Exception("No fields found")

			# Unpack the fields
			reading, meaning = unpack_reading(note[field_dict])

			# Check if no reading
			if reading == "":
				counts.no_reading += 1
				raise Exception("No reading found")

			# Update the fields
			note[field_read] = reading
			note[field_dict] = meaning

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
		'Notes without reading: {no_reading}\n'
		'Notes without fields: {no_fields}'
	).format(**counts.__dict__)

	if counts.edited < counts.total:
		info_msg += "\n\nTip: did you set the correct fields in the config?"

	showInfo(info_msg, title="Reading Unpacking Results")

	return
