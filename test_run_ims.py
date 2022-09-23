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
import sys

warnings.filterwarnings('ignore')
client = Client(nms_path=path_to_nms_client)
#client = Client(nms_path=path_to_nms_client, test_nms=False)
station = "USRK" # or multiple stations separated by comma. "SPA0,ARA0" 
station = "*" # or multiple stations separated by comma. "SPA0,ARA0" 
station = "HFS" # HAGFORS ARRAY, Sweden

#t0 = UTCDateTime('2022-07-07T'); t1 = t0; t2 = UTCDateTime('2022-07-07T01:00:00')
t0 = UTCDateTime('2022-03-05T00:13:26.10'); t1 = t0 - 100; t2 = t0 + 500

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
inventory = client.get_stations(station=station, starttime=t1, endtime=t2, use_cache=False)
#inventory = client.get_stations(station=station, longitude=lon0, latitude=lat0, maxradius=maxrad, use_cache=False)
#inventory = client.get_stations(minlongitude=0.0,maxlongitude=20.0,minlatitude=50.0,maxlatitude=70.0,use_cache=True)
#inventory = client.get_stations(station='seismic',minlongitude=0.0,maxlongitude=20.0,minlatitude=50.0,maxlatitude=70.0)
print(inventory)
#inventory.plot()

print('REQUESTING WAVEFORM DATA ...')
st = client.get_waveforms(station=station, channel='*Z*', starttime=t1, endtime=t2)
print(st)
#st.plot()

print('GET CHANNEL METADATA')
for tr in st:
    stakey = '%s.%s.%s.%s' % (tr.stats.network, tr.stats.station, tr.stats.location, tr.stats.channel)
    print('working on:', stakey)
    try:
        #sta = inventory.select(network=tr.stats.network, station=tr.stats.station, location=tr.stats.location, channel=tr.stats.channel)
        sta = inventory.select(network=tr.stats.network)
        print('###########1111', sta)
        sta = sta.get_channel_metadata(seed_id=stakey)
        print('###########2222', sta)
    except Exception as e:
        print('STOP: %s: %s' % (stakey, e))
        sys.exit()
    print(sta)

print('REQUESTING EVENT METADATA ...')
cat = client.get_events(starttime=t1, endtime=t2, minmagnitude=5.0, mindepth=20, maxdepth=100, minlongitude=0, maxlongitude=50)
print(cat)

