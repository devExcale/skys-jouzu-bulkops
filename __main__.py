import re

# Regex for extracting the accent section
re_accent = re.compile(r"<!-- accent_start -->(.*)<!-- accent_end -->")
# Regex to check whether there's an accent section at the end
re_accent_ends = re.compile(r"<!-- accent_start -->.*?<!-- accent_end -->$")
# Regex to find all svg/circle tags
re_tags = re.compile(r"</?(?:svg|circle).*?>")
# Regex to find global font tag with colour
re_font_color_start = re.compile(r"^<font color=\".*?\">(.*)$")

test_texts = [
	'<font color="#ff0000">あに<!-- accent_start --><br></font><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">あ</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">に</text><path d="m 16,5 35,25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,30 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="30" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="30" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->',
	'もとめる<!-- accent_start --><br><hr><br><svg class="pitch" width="172px" height="75px" viewBox="0 0 172 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">も</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">と</text><text x="75" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">め</text><text x="110" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">る</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 86,5 35,25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 121,30 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="121" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="156" cy="30" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="156" cy="30" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->',
	'<font color="#aaaaff">かえる<!-- accent_start --><br></font><hr><br><svg class="pitch" width="137px" height="75px" viewBox="0 0 137 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">か</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">え</text><text x="75" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">る</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 86,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="121" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="121" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->',
	'<font color="#a4a4ff">なかなか</font><!-- accent_start --><br><hr><br><svg class="pitch" width="172px" height="75px" viewBox="0 0 172 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">な</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">か</text><text x="75" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">な</text><text x="110" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">か</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 86,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 121,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="121" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="156" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="156" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->',
	'ば<!-- accent_start --><br><hr><br><svg class="pitch" width="67px" height="75px" viewBox="0 0 67 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">ば</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="51" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->',
]


def apply_colour(text: str, colour: str) -> str:
	"""
	Apply a colour to the text.
	:param text:
	:param colour:
	:return:
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


if __name__ == "__main__":
	for txt in test_texts:
		print(apply_colour(txt, "LEMIEPALLESONOBLU"))
