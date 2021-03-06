# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Tests the import_data.py script.

    Typical usage:

    python3 test_import.py
"""
import unittest
import pandas as pd
from import_data import StateGDPDataLoader

class USStateQuarterlyGDPImportTest(unittest.TestCase):
    def test_date_converter(self):
        """Tests the date converter function used to process raw data."""
        date_conv_fn = StateGDPDataLoader._date_to_obs_date

        self.assertEqual(date_conv_fn("2005:Q1"), "2005-03")
        self.assertEqual(date_conv_fn("2005:Q2"), "2005-06")
        self.assertEqual(date_conv_fn("2005:Q3"), "2005-09")
        self.assertEqual(date_conv_fn("2005:Q4"), "2005-12")
        self.assertEqual(date_conv_fn("1999:Q1"), "1999-03")
        self.assertEqual(date_conv_fn("2020:Q2"), "2020-06")

    def test_geoid_converter(self):
        """Tests the geoid converter function used to process raw data."""
        geoid_conv_fn = StateGDPDataLoader._convert_geoid

        self.assertEqual(geoid_conv_fn('   "1000"'), "geoId/10")
        self.assertEqual(geoid_conv_fn("1000"), "geoId/10")
        self.assertEqual(geoid_conv_fn("10"), "geoId/10")
        self.assertEqual(geoid_conv_fn("10    "), "geoId/10")
        self.assertEqual(geoid_conv_fn('10""""""'), "geoId/10")
        self.assertEqual(geoid_conv_fn("25100"), "geoId/25")
        self.assertEqual(geoid_conv_fn('   "760000"'), "geoId/76")
        self.assertEqual(geoid_conv_fn('123""""""'), "geoId/12")

    def test_data_processing_tiny(self):
        """Tests end-to-end data cleaning on a tiny example."""
        raw_df = pd.read_csv("test_tiny_raw.csv", index_col=0)
        clean_df = pd.read_csv("test_tiny_cleaned.csv", index_col=0)
        loader = StateGDPDataLoader()
        loader.process_data(raw_df)
        pd.testing.assert_frame_equal(clean_df, loader.clean_df)

    def test_data_processing_small(self):
        """Tests end-to-end data cleaning on a small example."""
        raw_df = pd.read_csv("test_small_raw.csv", index_col=0)
        clean_df = pd.read_csv("test_small_cleaned.csv", index_col=0)
        loader = StateGDPDataLoader()
        loader.process_data(raw_df)
        pd.testing.assert_frame_equal(clean_df, loader.clean_df)


if __name__ == '__main__':
    unittest.main()
