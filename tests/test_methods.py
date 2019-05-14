
import numpy as np
import pandas as pd

import trajpandas
from trajpandas import synthetic

def test_loop():
    df = synthetic.loops()

def test_straight_line():
    df = synthetic.straight_line()

def test_loop():
    df = synthetic.one_mile()

def test_delta():
    df = synthetic.straight_line()
    
    df.traj.add_delta()
    assert hasattr( df,"Dtime")
    df.traj.add_delta(Dxy=True)
    assert hasattr(df, "Dypos")
    df.traj.add_delta("lat")
    assert hasattr(df,"Dlat")
    df.traj.add_delta(["lat","lon"])
    assert hasattr(df, "Dlat")
    assert hasattr(df, "Dlon")

    ddf = df[df.id==df.id[0]]
    assert ddf.lat[10] - ddf.lat[9] == ddf.Dlat[10]
    assert ddf.lon[10] - ddf.lon[9] == ddf.Dlon[10]
    assert ddf.index[10] - ddf.index[9] == ddf.Dtime[10]

    
def test_interpolate():
    df = synthetic.loops()
    dd = trajpandas.interpolate(df)
    assert(len(df) ==  385)
    assert(len(dd) == 1519)

def test_piecewise_distance():
    """Test distance calculations"""
    dist = trajpandas.piecewise_distance([48.1372, 52.5186, 40.712777777778],
    	   		 	     [11.5756, 13.4083,-74.005833333333])
    assert all(np.round(dist,3) == np.array([ 504.216, 6385.264])) 

def test_add_dist_one_mile():
    dist1 = trajpandas.piecewise_distance([30,30+1/60],[0,0])[0] * 1000 
    df = synthetic.one_mile()
    df.traj.add_dist()
    dist2 = df.dist.iloc[-1]
    assert np.round(dist1,4) == np.round(dist2,4)

def test_add_dist_straight_line():
    df = synthetic.straight_line()
    df.traj.add_dist()
    assert len(df.dist.unique()) == 4
    assert np.sum(np.round(df.dist.unique(),4) ==
                  np.array([np.nan, 926.6244, 1604.9605, 1310.4448])) == 3   

def test_add_speed_one_mile():
    df = synthetic.one_mile()
    df.traj.add_speed()
    assert (round(df.speed[0],4) == 0.5148) and np.isnan(df.speed[1]) 
    df.traj.add_speed(t2=True)
    assert (round(df.speed[1],4) == 0.5148) and np.isnan(df.speed[0]) 

def test_add_speed_straight_line():
    df = synthetic.straight_line()
    df.traj.add_speed()
    assert np.all(np.round(df.speed.unique(),4)[:-1] ==
                  np.array([0.2574, 0.4458, 0.364 ]))   
