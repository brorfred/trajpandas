
import netCDF4

import trajpandas
from trajpandas import __version__


def test_version():
    assert __version__ == '0.1.1'


def model_latlon():
    nc = netCDF4.Dataset("tests/data/MOHID_lat_lon.nc")
    llat = nc.variables["lat"][:]
    llon = nc.variables["lon"][:]
    return llat,llon
    
def test_add_latlon():
    llat,llon = model_latlon()
    df = trajpandas.read_trm("tests/data/test_p000001_run.bin")
    df.traj.add_latlon(llat, llon)
    df.traj.setup_grid(llat, llon) 
    df.traj.add_latlon()
