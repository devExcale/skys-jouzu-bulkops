from typing import Dict, Any, Optional

from .utils import log


class AddonSettings:
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

		# Init root variables
		self.version = lookup_field(conf, "version", "")
		self.show_changelog = lookup_field(conf, "show_changelog", True)

		# Init UnpackConfig
		unpack_conf = lookup_field(conf, "unpack")
		self.unpack = UnpackSettings(unpack_conf)

		# Init PitchConfig
		pitch_conf = lookup_field(conf, "pitch")
		self.pitch = PitchSettings(pitch_conf)

		return

	def json(self):
		return {
			"version": self.version,
			"show_changelog": self.show_changelog,
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


class UnpackSettings:
	"""
	Class containing the configuration parameters for the unpacking operation.
	"""

	def __init__(
			self,
			conf: Optional[Dict[str, Any]] = None
	):
		self.changed = False

		self.field_dictionary = lookup_field(conf, "field_dictionary", "Meaning")

		self.field_reading = lookup_field(conf, "field_reading", "Reading")

		self.tag_fail = lookup_field(conf, "tag_fail", "bulkops::failed-unpack")

		return


class PitchSettings:
	"""
	Class containing the configuration parameters for the pitch colouring operation.
	"""

	def __init__(
			self,
			conf: Optional[Dict[str, Any]] = None
	):
		self.changed = False

		self.field_reading = lookup_field(conf, "field_reading", "Reading")

		self.fields_tocolour = lookup_field(conf, "fields_tocolour", ["Reading"])

		self.colour_heiban = lookup_field(conf, "colour_heiban", "#a4a4ff")

		self.colour_atamadaka = lookup_field(conf, "colour_atamadaka", "red")

		self.colour_nakadaka = lookup_field(conf, "colour_nakadaka", "green")

		self.colour_oodaka = lookup_field(conf, "colour_oodaka", "orange")

		self.tag_fail = lookup_field(conf, "tag_fail", "bulkops::failed-pitch")

		self.colour_graph = lookup_field(conf, "colour_graph", False)

		return


def lookup_field(d: Dict[str, Any], key: str, default: Any = None) -> Any:
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
		return default

	# Check if key is not in dictionary
	if key not in d:
		return default

	# Return value
	return d[key]
