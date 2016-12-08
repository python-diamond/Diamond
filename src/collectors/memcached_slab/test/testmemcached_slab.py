import os
import sys
import unittest

# Make sure we can import the collector, which lives in the directory above.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import memcached_slab


RAW_SLAB_STATS = """STAT 1:chunk_size 96\r
STAT 1:chunks_per_page 10922\r
STAT active_slabs 1\r
STAT total_malloced 1048512\r
END\r
"""


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
