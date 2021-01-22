import os
import glob
import tsbb15_labs.lab3 as lab3
from tsbb15_labs import IMAGE_DIRECTORY
import PIL


def test_stereo_pair():
    pair = lab3.load_stereo_pair()
    assert len(pair) == 2
    assert pair[0].shape == (683,1024)
