#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Data request from the ETHZ network
http://www.fdsn.org/networks/detail/CH/


NOTE CH network has accelerometer data (HG) but it doesn't seem to always have
"dip" so our scripts break. For example see error below
-----
...
Traceback (most recent call last):
  File "gw_ethz.py", line 75, in <module>
    ev_info.run_get_waveform()
  File "/home/calvizur/REPOSITORIES/pyseis/getwaveform.py", line 358, in run_get_waveform
    rotate_and_write_stream(st2, evname_key, self.icreateNull, self.rotateUVW)
  File "/home/calvizur/REPOSITORIES/pyseis/util_write_cap.py", line 144, in rotate_and_write_stream
    substr[itr].stats.sac['cmpinc'] = dip1 + 90.0
TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'
-----


20170816 -- calvizuri <celso.alvizuri@unil.ch>
"""

from getwaveform import *
import sys

#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_ch2017_uri.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_ch2017_sierreVS.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_landslide_ch20040918.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_landslide_ch20060726.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_landslide_ch.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_landslide_ch-subset.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_landslide_ch-subset3.txt"
#events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_landslide_it_formazza"
events_file="/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_ch2017_landslide.txt"

fid = open(events_file, "r")
data = fid.readlines()
fid.close()

ev_info = getwaveform()
ev_info.idb = 1     # NOTE idb=5 for for SED-ETHZ data causes an error
ev_info.ifsave_stationxml = False   # this causes errors so I disable for now
ev_info.overwrite_ddir = 0       # delete data dir if it exists
ev_info.use_catalog = 0          # event catalog for source parameters
ev_info.min_dist = 0
ev_info.max_dist = 2000
ev_info.tbefore_sec = 100
ev_info.tafter_sec = 2000
ev_info.scale_factor = 100 
ev_info.resample_TF = True
#ev_info.resample_freq = 40
ev_info.resample_freq = 20  # new, 2018-11-28
#ev_info.user = 'bhutan1156arc'
#ev_info.password = 'bhutan1156arc'

# NOTE network PN is disabled since a station with missing deconv info crashes the scripts (when doing a full-station search for available data)
# To see this add "print(station)" as line 238 in /home/calvizur/UTILS/anaconda3/envs/seis/lib/python3.6/site-packages/obspy/io/stationxml/core.py 
#ev_info.channel = '*,-HH?,-BH?,-LH?'
#ev_info.network = 'IU,-PN,-IM' # 
ev_info.network = '-CH' # all BUT CH
ev_info.network = '*' # CH
ev_info.station = '*'
#ev_info.channel = 'HH?,BH?,LH?' 
#ev_info.channel = 'HH?'  # WORKS for INGV: LH. No BH HH
ev_info.channel = 'LH?'  # WORKS for ODC/ORFEUS: LH
#ev_info.channel = '*'

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

