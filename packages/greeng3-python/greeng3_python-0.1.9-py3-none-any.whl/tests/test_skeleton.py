import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestTestSkeleton(unittest.TestCase):

	def test_skeleton(self):
		self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
