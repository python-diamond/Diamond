import os
import unittest

import memcached_slab


fixtures = os.path.join(os.path.dirname(__file__), 'fixtures', 'stats')
with open(fixtures, 'rb') as f:
    RAW_SLAB_STATS = f.read()


class MemcachedSlabCollectorTestCase(unittest.TestCase):

    def test_dict_to_paths(self):
        dict_ = {
            'foo': {
                1: {
                    'baz': 1,
                    'bam': 2,
                },
            },
            'car': 3,
        }
        metrics = memcached_slab.dict_to_paths(dict_)
        self.assertEqual(metrics['foo.1.baz'], 1)
        self.assertEqual(metrics['foo.1.bam'], 2)
        self.assertEqual(metrics['car'], 3)

    def test_parse_slab_stats(self):
        slab_stats = memcached_slab.parse_slab_stats(RAW_SLAB_STATS)
        self.assertEqual(slab_stats['slabs'][1]['chunk_size'], 96)
        self.assertEqual(slab_stats['slabs'][1]['chunks_per_page'], 10922)
        self.assertEqual(slab_stats['active_slabs'], 1)
        self.assertEqual(slab_stats['total_malloced'], 1048512)


if __name__ == '__main__':
    unittest.main()
