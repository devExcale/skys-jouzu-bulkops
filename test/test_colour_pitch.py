from unittest import TestCase

from src.pitch import apply_colour_to_field


class TestColourPitch(TestCase):

	def test_noaccent(self):
		x = '<font color="white">ので</font>'

		y = '<font color="#a4a4ff">ので</font>'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff"), y)

	def test_noaccent_nofont(self):
		x = 'ので'

		y = '<font color="#a4a4ff">ので</font>'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff"), y)

	def test_accent_nofont_nograph(self):
		x = 'いく<!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		y = '<font color="#a4a4ff">いく</font><!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff"), y)

	def test_accent_font_nograph(self):
		x = '<font color="white">いく</font><!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		y = '<font color="#a4a4ff">いく</font><!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff"), y)

	def test_useraccent_nofont_nograph(self):
		x = 'いく<!-- user_accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		y = '<font color="#a4a4ff">いく</font><!-- user_accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff"), y)

	def test_useraccent_font_nograph(self):
		x = '<font color="white">いく</font><!-- user_accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		y = '<font color="#a4a4ff">いく</font><!-- user_accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff"), y)

	def test_accent_nofont_wgraph(self):
		x = 'いく<!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		y = '<font color="#a4a4ff">いく</font><!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#a4a4ff !important;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#a4a4ff !important;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#a4a4ff !important;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#a4a4ff !important;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#a4a4ff !important;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#a4a4ff !important;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#a4a4ff !important;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff", colour_graph=True), y)

	def test_accent_font_wgraph(self):
		x = '<font color="white">いく</font><!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#000;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#000;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#000;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#000;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#000;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#000;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		y = '<font color="#a4a4ff">いく</font><!-- accent_start --><br><hr><br><svg class="pitch" width="102px" height="75px" viewBox="0 0 102 75"><text x="5" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#a4a4ff !important;">い</text><text x="40" y="67.5" style="font-size:20px;font-family:sans-serif;fill:#a4a4ff !important;">く</text><path d="m 16,30 35,-25" style="fill:none;stroke:#a4a4ff !important;stroke-width:1.5;"></path><path d="m 51,5 35,0" style="fill:none;stroke:#a4a4ff !important;stroke-width:1.5;"></path><circle r="5" cx="16" cy="30" style="opacity:1;fill:#a4a4ff !important;"></circle><circle r="5" cx="51" cy="5" style="opacity:1;fill:#a4a4ff !important;"></circle><circle r="5" cx="86" cy="5" style="opacity:1;fill:#a4a4ff !important;"></circle><circle r="3.25" cx="86" cy="5" style="opacity:1;fill:#fff;"></circle></svg><!-- accent_end -->'

		self.assertEqual(apply_colour_to_field(x, "#a4a4ff", colour_graph=True), y)
