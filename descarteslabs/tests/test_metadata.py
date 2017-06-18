# Copyright 2017 Descartes Labs.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import itertools
import unittest

import descarteslabs as dl


class TestMetadata(unittest.TestCase):
    instance = None

    @classmethod
    def setUpClass(cls):
        cls.instance = dl.metadata

    def test_sources(self):
        r = self.instance.sources()
        self.assertGreater(len(r), 0)

    def test_search(self):
        r = self.instance.search()
        self.assertGreater(len(r['features']), 0)

    def test_search_dltile(self):
        dltile = "256:16:30.0:15:-11:591"
        r = self.instance.search(start_time='2016-07-06', end_time='2016-07-07',
                                 const_id=['L8'], dltile=dltile)
        ids = [f['id'] for f in r['features']]
        self.assertTrue('meta_LC80270312016188_v1' in ids)

    def test_sat_id(self):
        r = self.instance.search(start_time='2016-07-06', end_time='2016-07-07', sat_id='LANDSAT_8')
        self.assertGreater(len(r['features']), 0)

    def test_cloud_fraction(self):
        r = self.instance.search(start_time='2016-07-06', end_time='2016-07-07', sat_id='LANDSAT_8',
                                 cloud_fraction=0.5)
        for feature in r['features']:
            self.assertLess(feature['properties']['cloud_fraction'], 0.5)

        r = self.instance.search(start_time='2016-07-06', end_time='2016-07-07', sat_id='LANDSAT_8',
                                 cloud_fraction=0.0)
        for feature in r['features']:
            self.assertEqual(feature['properties']['cloud_fraction'], 0.0)

    def test_const_id(self):
        r = self.instance.search(start_time='2016-07-06', end_time='2016-07-07', const_id=['L8'])
        self.assertGreater(len(r['features']), 0)

    def test_multiple_const_id(self):
        r = self.instance.search(start_time='2016-07-06', end_time='2016-07-07', const_id=['L8', 'L7'])
        self.assertGreater(len(r['features']), 0)

    def test_place(self):
        r = self.instance.search(const_id=['L8'], place='north-america_united-states_iowa', limit=1)
        self.assertEqual(1, len(r['features']))

    def test_summary(self):
        r = self.instance.summary(start_time='2016-07-06', end_time='2016-07-07', const_id=['L8'])
        self.assertIn('const_id', r)
        self.assertIn('count', r)
        self.assertIn('pixels', r)
        self.assertIn('bytes', r)
        self.assertGreater(r['count'], 0)

    def test_summary_part(self):
        r = self.instance.summary(start_time='2016-07-06', end_time='2016-07-07', const_id=['L8'], part='year')
        self.assertIn('const_id', r)
        self.assertIn('count', r)
        self.assertIn('pixels', r)
        self.assertIn('bytes', r)
        self.assertIn('items', r)
        self.assertEqual(len(r['items']), 1)

    def test_features(self):
        r = self.instance.features(start_time='2016-07-06', end_time='2016-07-07', sat_id='LANDSAT_8', limit=20)
        first_21 = itertools.islice(r, 21)
        self.assertGreater(len(list(first_21)), 0)


if __name__ == '__main__':
    unittest.main()
