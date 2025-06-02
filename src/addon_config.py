from typing import Dict, Any, Optional

from .utils import log


class AddonConfig:
	"""
	Class containing the configuration parameters for the addon.
	"""

	def __init__(
			self,
			conf: Optional[Dict[str, Any]] = None,
	):
		"""
		Initializes the AddonConfig class and loads the configuration.
		If no configuration is provided or any field is missing, it will use the default values.

		:param conf: dictionary with configuration values
		"""

		log("Loading config...")

		self.changed = False

		# Init UnpackConfig
		unpack_conf, b_write = lookup_field(conf, "unpack")
		self.unpack = UnpackConfig(unpack_conf)
		self.changed |= b_write

		# Init PitchConfig
		pitch_conf, b_write = lookup_field(conf, "pitch")
		self.pitch = PitchConfig(pitch_conf)
		self.changed |= b_write

		# Check if any of the subconfigs needs to be overwritten
		self.changed |= self.unpack.changed or self.pitch.changed

		return

	def json(self):
		return {
			"unpack": {
				"field_dictionary": self.unpack.field_dictionary,
				"field_reading": self.unpack.field_reading,
				"tag_fail": self.unpack.tag_fail,
			},
			"pitch": {
				"field_reading": self.pitch.field_reading,
				"fields_tocolour": self.pitch.fields_tocolour,
				"colour_heiban": self.pitch.colour_heiban,
				"colour_atamadaka": self.pitch.colour_atamadaka,
				"colour_nakadaka": self.pitch.colour_nakadaka,
				"colour_oodaka": self.pitch.colour_oodaka,
				"tag_fail": self.pitch.tag_fail,
				"colour_graph": self.pitch.colour_graph,
			}
		}


class UnpackConfig:
	"""
	Class containing the configuration parameters for the unpacking operation.
	"""

	def __init__(
			self,
			conf: Optional[Dict[str, Any]] = None
	):
		self.changed = False

		self.field_dictionary, b_write = lookup_field(conf, "field_dictionary", "Meaning")
		self.changed |= b_write

		self.field_reading, b_write = lookup_field(conf, "field_reading", "Reading")
		self.changed |= b_write

		self.tag_fail, b_write = lookup_field(conf, "tag_fail", "bulkops::failed-unpack")
		self.changed |= b_write

		return


class PitchConfig:
	"""
	Class containing the configuration parameters for the pitch colouring operation.
	"""

	def __init__(
			self,
			conf: Optional[Dict[str, Any]] = None
	):
		self.changed = False

		self.field_reading, b_write = lookup_field(conf, "field_reading", "Reading")
		self.changed |= b_write

		self.fields_tocolour, b_write = lookup_field(conf, "fields_tocolour", ["Reading"])
		self.changed |= b_write

		self.colour_heiban, b_write = lookup_field(conf, "colour_heiban", "#a4a4ff")
		self.changed |= b_write

		self.colour_atamadaka, b_write = lookup_field(conf, "colour_atamadaka", "red")
		self.changed |= b_write

		self.colour_nakadaka, b_write = lookup_field(conf, "colour_nakadaka", "green")
		self.changed |= b_write

		self.colour_oodaka, b_write = lookup_field(conf, "colour_oodaka", "orange")
		self.changed |= b_write

		self.tag_fail, b_write = lookup_field(conf, "tag_fail", "bulkops::failed-pitch")
		self.changed |= b_write

		self.colour_graph, b_write = lookup_field(conf, "colour_graph", False)
		self.changed |= b_write

		return


def lookup_field(d: Dict[str, Any], key: str, default: Any = None) -> (Any, bool):
	"""
	Tries to retrieve the value of a key from a dictionary.
	If the key is present, the value is returned and the flag return value is False;
	otherwise, the default value is returned and the flag return value is True.

	:param d: dictionary to search
	:param key: key to search for
	:param default: default value to return
	:return: a tuple containing the value and the flag
	"""

	# Check if dictionary is empty/None
	if not d:
		return default, True

	# Check if key is not in dictionary
	if key not in d:
		return default, True

	# Return value
	return d[key], False
