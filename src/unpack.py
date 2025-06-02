import re
from typing import Tuple

# Regex for extracting the reading (hiragana) this format: e.g. "たる【足る】 ★★★★"
re_reading = re.compile(r"(.*).*【.*】.*")


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
