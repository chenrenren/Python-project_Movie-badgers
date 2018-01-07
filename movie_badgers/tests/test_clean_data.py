import sys
import unittest
import os
sys.path.append('../')
import clean_data as cd   # noqa


class FunctionRunTest(unittest.TestCase):
    """Test if functions run succesfully with correct input"""

    def test_get_act_pop_avg(self):
        cd.get_act_pop_avg()

    def test_clean_director_actor(self):
        cd.clean_director_actor()

    def test_clean_regression_data(self):
        cd.clean_regression_data()


if __name__ == '__main__':
    unittest.main()
