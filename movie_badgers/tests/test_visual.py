import unittest
import sys
import os
sys.path.append("..//")
from movie_plot import *   # noqa

path = os.getcwd()
input1 = "revenue"
input2 = "budget"
input3 = "imdb_votes"
input4 = "released_on_dump_month"


class ModelTest(unittest.TestCase):

    def test_model(self):
        scatter_plot(path, input2, input1)
        scatter_plot(path, input2, input3)
        box_plot(path, input4)
