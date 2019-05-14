

import numpy as np
import pandas as pd

import trajpandas
from trajpandas import synthetic
from trajpandas.utils import grid

def test_heatmat():
    df = synthetic.loops()
    hmat = grid.heatmat(df)
    assert np.sum(hmat) == len(df)
    assert np.all(sorted(set(np.nonzero(hmat>0)[1])) ==
                  sorted(set(df.xpos.values.astype(int))))
    assert np.all(sorted(set(np.nonzero(hmat>0)[0])) ==
                  sorted(set(df.ypos.values.astype(int))))
    
    df = synthetic.straight_line()
    hmat = grid.heatmat(df)
    assert np.sum(hmat) == len(df)
    assert np.all(sorted(set(np.nonzero(hmat>0)[1])) ==
                  sorted(set(df.xpos.values.astype(int))))
    assert np.all(sorted(set(np.nonzero(hmat>0)[0])) ==
                  sorted(set(df.ypos.values.astype(int))))

