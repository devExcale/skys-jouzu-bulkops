import re
from typing import Tuple

# Regex for extracting the reading (hiragana) this format: e.g. "たる【足る】 ★★★★"
re_reading_legacy = re.compile(r"^.*?([一-龠ぁ-ゔァ-ヴーa-zA-Z0-9ａ-ｚＡ-Ｚ０-９々〆〤ヶ]+)【.*?】.*?$")

# Regex for extracting the reading (hiragana) this format: e.g. "足る (たる) ★★★★"
re_reading_modern = re.compile(r"^.*?\(([一-龠ぁ-ゔァ-ヴーa-zA-Z0-9ａ-ｚＡ-Ｚ０-９々〆〤ヶ]+)\).*?$")

# Regex for extracting the reading (hiragana) this format: e.g. "たる ★★★★"
re_reading_plain = re.compile(r"^.*?([一-龠ぁ-ゔァ-ヴーa-zA-Z0-9ａ-ｚＡ-Ｚ０-９々〆〤ヶ]+).*?$")


def unpack_reading(content: str) -> Tuple[str, str]:
	"""
	Unpack the content of a field into reading and meaning.
	If the content cannot be parsed, an empty string is returned for the reading and the meaning is returned as is;
	otherwise, the reading and the meaning (minus the reading) are returned.

	:param content: The content of the field
	:return: A tuple containing the reading and meaning
	"""

	# Split on newline
	split_content = content.split("<br>")
	n_lines = len(split_content)

	# First line contains reading
	expression = split_content[0]

	# Count the contiguous new lines after the expressions
	leading_lfs = 1
	while leading_lfs < n_lines and not split_content[leading_lfs].strip():
		leading_lfs += 1

	# Extract the reading (legacy)
	match = re_reading_legacy.search(expression)

	# Extract the reading (modern)
	if not match:
		match = re_reading_modern.search(expression)

	# Extract the reading (plain)
	if not match:
		match = re_reading_plain.search(expression)

	# No match
	if not match:
		return "", content

	reading = match.group(1)

	# The rest is the meaning
	meaning = '<br>'.join(split_content[leading_lfs:])

	return reading, meaning
