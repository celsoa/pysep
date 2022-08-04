#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
Test fetch IMS data using seismonpy

20220708 TODO: add way to correct for instrument response

See notebook from Andreas K for examples
http://localhost:8888/notebooks/ims_data_request.ipynb

20220706 -- cralvizuri <celso.alvizuri@gmail.com>
"""

path_to_nms_client = '/nobackup/celso/REPOSITORIES/IMS-nms_client3/nms_client3'

print('Initializing seismonpy-IMS interface')
from obspy import UTCDateTime
from seismonpy.utils.ims_request import IMS_Client as Client
from obspy.geodetics import kilometer2degrees
import warnings

warnings.filterwarnings('ignore')
client = Client(nms_path=path_to_nms_client)
#client = Client(nms_path=path_to_nms_client, test_nms=False)
station = "USRK" # or multiple stations separated by comma. "SPA0,ARA0" 
station = "*" # or multiple stations separated by comma. "SPA0,ARA0" 

#print('REQUESTING STATION INVENTORY ...')
#inventory=client.get_stations(station=station)
#print(inventory)
##print(inventory[0][-1][0].response)

#inventory=client.get_stations(station="hydroacoustic")
#inventory.plot();

print('REQUESTING STATION INVENTORY ...')
#station='seismic'   # can be hydroacoustic, infrasound <-- 'station' could be renamed, eg 'datatype' 'stationtype'
lon0, lat0 = 132.0, 44.2  # station USRK
maxrad_km = 2
lon0, lat0 = 129.0, 41.3  # NK test site
maxrad_km = 2000     # include USRK, KSRS
maxrad = kilometer2degrees(maxrad_km)
#inventory=client.get_stations(station=station,use_cache=True)
inventory=client.get_stations(station=station, longitude=lon0, latitude=lat0, maxradius=maxrad, use_cache=False)
#inventory=client.get_stations(minlongitude=0.0,maxlongitude=20.0,minlatitude=50.0,maxlatitude=70.0,use_cache=True)
#inventory=client.get_stations(station='seismic',minlongitude=0.0,maxlongitude=20.0,minlatitude=50.0,maxlatitude=70.0)
print(inventory)
inventory.plot()

print('REQUESTING WAVEFORM DATA ...')
st=client.get_waveforms(station=station,channel='*Z*',starttime=UTCDateTime('2022-07-07T'),endtime=UTCDateTime('2022-07-07T01:00:00'))
print(st)
st.plot();

print('REQUESTING EVENT METADATA ...')
cat=client.get_events(starttime=UTCDateTime('2022-01-01T'),endtime=UTCDateTime('2022-06-30T'),minmagnitude=5.0,mindepth=20,maxdepth=100,minlongitude=0,maxlongitude=50)
print(cat)
