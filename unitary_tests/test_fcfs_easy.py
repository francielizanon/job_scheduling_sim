#!/usr/bin/env python3

import unittest
import sys
# Add the parent directory to the path so we can import
# code from our simulator
sys.path.append('../')

from simulator.engine import Engine              # noqa


class FCFSEasyTest(unittest.TestCase):
    def test_10000_nodes(self):
        simulator = Engine('fcfs_easy', 10000, -1, '../ANL-Intrepid-2009-1.swf')
        makespan = simulator.run()
        self.assertEqual(makespan, 30908522)

    def test_10000_tasks(self):
        simulator = Engine('fcfs_easy', 40960, 10000, '../ANL-Intrepid-2009-1.swf')
        makespan = simulator.run()
        self.assertEqual(makespan, 3610649)

    def test_10000_tasks_and_nodes(self):
        simulator = Engine('fcfs_easy', 10000, 10000, '../ANL-Intrepid-2009-1.swf')
        makespan = simulator.run()
        self.assertEqual(makespan, 4844621)


if __name__ == '__main__':
    unittest.main()
