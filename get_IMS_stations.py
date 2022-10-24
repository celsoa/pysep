#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

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
from obspy.geodetics import kilometer2degrees
from seismonpy.utils.ims_request import IMS_Client
client = IMS_Client(nms_path=path_to_nms_client)

station = "USRK" # or multiple stations separated by comma. "SPA0,ARA0" 
station = "*" # or multiple stations separated by comma. "SPA0,ARA0" 
print('REQUESTING STATION INVENTORY ...')
lon0, lat0 = 132.0, 44.2  # station USRK
maxrad_km = 2
#lon0, lat0 = 129.0, 41.3  # NK test site
#maxrad_km = 2000     # include USRK, KSRS
otime = UTCDateTime("2020-05-18T01:11:55.328")
t1 = otime-100
t2 = otime+100

# * * *H* 2020-05-18T01:10:15.328000Z 2020-05-18T01:20:15.328000Z 20.1931 67.7951 0.0 13.489824088780958 True
t1 = UTCDateTime("2020-05-18T01:10:15.328000Z")
t2 = UTCDateTime("2020-05-18T01:20:15.328000Z")
minrad, maxrad = 0, kilometer2degrees(maxrad_km)

inventory = client.get_stations(
        network    = '*', 
        station    = station, 
        channel    = "*H*",
        starttime  = t1, 
        endtime    = t2,
        longitude  = lon0,
        latitude   = lat0,
        minradius  = kilometer2degrees(minrad),
        maxradius  = kilometer2degrees(maxrad),
        use_cache  = True,    
        cache_file = '/nobackup/celso/REPOSITORIES/pysep-dev-IMS/ims_full_inventory.p'
        # 2022-07-19 NOTE! unable to get station info if
        # using local cache! either sta data changed in
        # the last few days or there is a bug in cached
        # file!
)
print('\nInventory\n', inventory)
inventory.plot()

