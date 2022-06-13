#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Data request for the 2017 NK event

20170816 -- calvizuri <celso.alvizuri@unil.ch>
"""

from getwaveform import *
import sys

#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk2016.txt"   # nuc
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk2016-q.txt" # quake
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk2016-c.txt" # collapse?
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk2006.txt" # earliest 
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk.txt" # earliest 
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk_zhao" # main ref (2018-04-16)
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk_quakes_usgs"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk_usgs2"  # Main+collapse (2018-04-16)
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk_try"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk6_usgs"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk_quakes_usgs2"
events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_nk_geothr_usgs"    # Nk geothermal #2

fid = open(events_file, "r")
data = fid.readlines()
fid.close()

ev_info = getwaveform()
ev_info.idb = 1
ev_info.ifsave_stationxml = False   # this causes errors so I disable for now
ev_info.overwrite_ddir = 1       # delete data dir if it exists
ev_info.use_catalog = 0          # event catalog for source parameters
ev_info.min_dist = 0
ev_info.max_dist = 3000
ev_info.tbefore_sec = 100
ev_info.tafter_sec = 3000
ev_info.scale_factor = 100 
ev_info.resample_TF = True
ev_info.resample_freq = 20  # 2018-05-07 new: 20. Old: 40
#ev_info.user = 'bhutan1156arc'
#ev_info.password = 'bhutan1156arc'

# NOTE network PN is disabled since a station with missing deconv info crashes the scripts (when doing a full-station search for available data)
# To see this add "print(station)" as line 238 in /home/calvizur/UTILS/anaconda3/envs/seis/lib/python3.6/site-packages/obspy/io/stationxml/core.py 
#ev_info.channel = '*,-HH?,-BH?,-LH?'
#ev_info.network = 'IU,-PN,-IM' # 
#ev_info.channel = 'HH?,BH?,LH?'
#ev_info.network = '*,-PN'

# 2017-12-20 ISSUES when requesting all channels ('*'):
#   No data available for request (nk06 event): IM JP KG SY
#   div/0 error: network XG 
#   event 2017-11-15 station MG04.XL: Could not find a valid Response Stage Type 
#   event 2017-11-15: Exception: Can't merge traces with same ids but differing sampling rates! -- station BUS2, channel BH (S. korea)
# ev_info.network = 'XG'
# ev_info.station = 'STZ'
#ev_info.channel = '*' 
#ev_info.station = '*,-BUS2,-MG04' # event NK 2017-11-15 avoid BUS2. see exception above
ev_info.channel = 'HH?,BH?,LH?'
ev_info.network = '*,-PN,-XL'

## TEMP -- for testing single stations/net/..
#ev_info.network = 'IU'
#ev_info.station = 'SSPA'
#ev_info.channel = 'BH?'
##ev_info.location = '00'


#-----------------------------------------------------------
# build list of event info
#-----------------------------------------------------------
ev_info_list = []
for row in data:
    line = row.split()
    iev_info = ev_info.copy()
    iev_info.otime = obspy.UTCDateTime(line[0])
    iev_info.elon = line[1]
    iev_info.elat = line[2]
    iev_info.edep = line[3]
    iev_info.emag = line[4]

    iev_info.evname = util_helpers.otime2eid(iev_info.otime)
    iev_info.get_events_client()

    #-----------------------------------------------------------
    # append event to list
    # append getwaveform objects
    ev_info_list.append(iev_info)
    #-----------------------------------------------------------

#-----------------------------------------------------------
# run extraction
#-----------------------------------------------------------
nev = len(ev_info_list)
for ii in range(nev):
    ev_info = ev_info_list[ii]
    ev_info.get_events_client()
    ev_info.run_get_waveform()

