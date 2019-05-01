
import numpy as np
import pandas as pd

import trajpandas

def read_synthetic():
    index = pd.date_range(start="2018-01-01", end="2018-01-10",freq="4h")
    dflist = []
    for num in range(1,8):
        tpos = np.linspace(0, np.pi*5, len(index))
        xpos = (np.sin(tpos) + tpos*0.1*num)
        ypos = (np.cos(tpos) * 3) +8
        trid = (xpos * 0 + num).astype(int)
        df = pd.DataFrame(index=index, data={"id":trid,"xpos":xpos,"ypos":ypos})
        dflist.append(df)
    df = pd.concat(dflist)
    df.sort_index(inplace=True)

    llat,llon = np.mgrid[35:35.05:0.001, -55:-54.95:0.001]
    df.traj.setup_grid(llat, llon)
    df.traj.add_latlon()
    return df

def read_synthetic_straight_line():
    index = pd.date_range(start="2018-01-01", end="2018-01-02",freq="1h")
    lon  = np.arange(-20,-20+(1/60)*25,1/60)[:25]
    xpos = np.arange(1,26)
    def dfline(trid, ypos, lat):
        return pd.DataFrame({"id":trid,
            "xpos":xpos, "ypos":ypos, "lon":lon, "lat":lat}, index=index)

    df1 = dfline(1, np.arange(60,60+25), 60)
    df2 = dfline(2, np.arange(45,45+25), 45)
    df3 = dfline(3, np.arange(30,30+25), 30)
    return pd.concat([df1,df2,df3]).sort_index()

def synthetic_one_mile():
     index = pd.date_range(start="2018-01-01", end="2018-01-02",freq="1h")[:2]
     xpos = [1,1]
     ypos = [1,2]
     lat  = [30,30+1/60]
     lon  = [0,0]
     return pd.DataFrame(
         {"id":1, "xpos":xpos, "ypos":ypos, "lon":lon, "lat":lat}, index=index)

def test_interpolate():
    df = read_synthetic()
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
    df = synthetic_one_mile()
    df.traj.add_dist()
    dist2 = df.dist.iloc[-1]
    assert np.round(dist1,4) == np.round(dist2,4)

def test_add_dist_straight_line():
    df = read_synthetic_straight_line()
    df.traj.add_dist()
    assert len(df.dist.unique()) == 4
    assert np.sum(np.round(df.dist.unique(),4) ==
                  np.array([np.nan, 926.6244, 1604.9605, 1310.4448])) == 3   

def test_add_speed_one_mile():
    df = synthetic_one_mile()
    df.traj.add_speed()
    assert (round(df.speed[0],4) == 0.5148) and np.isnan(df.speed[1]) 
    df.traj.add_speed(t2=True)
    assert (round(df.speed[1],4) == 0.5148) and np.isnan(df.speed[0]) 

def test_add_speed_straight_line():
    df = read_synthetic_straight_line()
    df.traj.add_speed()
    assert np.all(np.round(df.speed.unique(),4)[:-1] ==
                  np.array([0.2574, 0.4458, 0.364 ]))   
