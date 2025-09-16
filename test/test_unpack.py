import csv
import logging
from typing import Dict
from unittest import TestCase

from src.unpack import unpack_reading

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TestUnpack(TestCase):
	"""
	Test suite for the unpacking functionality.
	"""

	def test_unpack(self) -> None:
		"""
		Tests the unpack_reading functionality.
		Reads test cases from CSV files unpack_x.csv and unpack_y.csv in data folder.

		:return: ``None``
		"""

		# Get file paths
		x_path = 'test/data/unpack_x.csv'
		y_path = 'test/data/unpack_y.csv'

		# Open files for reading
		with open(x_path, 'r', encoding='utf-8') as x_file, open(y_path, 'r', encoding='utf-8') as y_file:
			# Read data from CSV files
			x_reader = csv.DictReader(x_file)
			y_reader = csv.DictReader(y_file)

			# Iterate over rows in both files
			for x_row, y_row in zip(x_reader, y_reader):
				x_id = x_row['Note ID']
				x_expression = x_row['Expression']

				# Run subtest
				with self.subTest(msg=f'Unpack {x_id}: {x_expression}'):
					self._test_unpack_row(x_row, y_row)

		return

	def _test_unpack_row(self, x_row: Dict[str, str], y_row: Dict[str, str]) -> None:
		"""
		Tests a single row of the unpacking function. See ``TestUnpack.test_unpack`` for details.

		:param x_row: Row from unpack_x.csv
		:param y_row: Row from unpack_y.csv
		:return: ``None``
		"""

		logging.info(f'Testing Note ID {x_row["Note ID"]}')

		x_id = x_row['Note ID']
		y_id = y_row['Note ID']
		x_expression = x_row['Expression']
		y_expression = y_row['Expression']

		# Ensure same id and expression
		self.assertEqual(x_id, y_id, f'Different Note ID')
		self.assertEqual(x_expression, y_expression, f'Different Expression')

		x_meaning = x_row['Meaning']
		y_meaning = y_row['Meaning']
		y_reading = y_row['Reading']

		# Call unpack
		x_reading, x_meaning = unpack_reading(x_meaning)

		self.assertEqual(x_reading, y_reading, f'Different Reading')
		self.assertEqual(x_meaning, y_meaning, f'Different Meaning')

		return
