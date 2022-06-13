#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
list of events for the himfmt project

20170816 -- calvizuri <celso.alvizuri@unil.ch>
"""

from getwaveform import *
import sys

events_file="/home/calvizur/REPOSITORIES/projects/himfmt/data/HIMNT_subset_dep50-100.txt"
events_file="/home/calvizur/REPOSITORIES/projects/himfmt/data/HIMNT_subset_n5.txt"
events_file="/home/calvizur/REPOSITORIES/projects/himfmt/data/HIMNT_subset_dlt3.txt"
events_file="/home/calvizur/REPOSITORIES/projects/himfmt/data/HIMNT_subset_dlt3temp.txt"
events_file="/home/calvizur/REPOSITORIES/projects/himfmt/data/HIMNT_DC_candidates"  # 2018-07-13 -- DC candidates
events_file="/home/calvizur/REPOSITORIES/projects/himfmt/data/HIMNT_DC_candidate1"  # 2018-07-13 -- DC candidates
# 2002-05-08T17:56:59.380000Z   86.488500   28.582500  75.92  4.17   34  0.29
# 2002-06-28T17:44:16.150000Z   87.485000   27.760000  65.61  4.15   35  0.20
# 2002-10-02T07:28:08.700000Z   86.717500   28.614333  61.44  3.79   12  0.10
fid = open(events_file, "r")
data = fid.readlines()
fid.close()

ev_info = getwaveform()
ev_info.idb = 1
ev_info.ifsave_stationxml = False   # this causes errors so I disable for now
ev_info.overwrite_ddir = 1       # delete data dir if it exists
ev_info.use_catalog = 0          # do not use event catalog for source parameters
ev_info.min_dist = 0
ev_info.max_dist = 1000
ev_info.tbefore_sec = 100
ev_info.tafter_sec = 600
ev_info.scale_factor = 100 
ev_info.resample_TF = True
ev_info.resample_freq = 40        
# NOTE station PPWIN.PN is disabled since it's missing deconv info and it crashes the scripts (when doing a full-station search for available data)
# To see this add "print(station)" as line 238 in /home/calvizur/UTILS/anaconda3/envs/seis/lib/python3.6/site-packages/obspy/io/stationxml/core.py 
# NOTE IC XA YL are the only networks returned within a 1000-km radius of the time of the HIM main event
# NOTE SY are Synthetic Seismograms (!) -- IRIS'
# NOTE Main ev# 2.
#           Net XA, -- PARO produces error: ZeroDivisionError: float division by zero 
#                   -- BUMT, TASH did not return data
#           Net CB (China) -- CAD, KSH, NAQ, TNC. None returned data
#           Net XC -- NB01 NB02 NB03 NB04 NB05 NB06 NB07 NB08. None returned data
# NOTE Main ev# 3.
#           net CB not available
           
ev_info.channel = '*'

# event 1 -- MAIN
ev_info.network = 'IC,XA,YL'
ev_info.network = '*,-PN,-SY'

# # event 2
# ev_info.network = '*,-PN,-SY,-XC' 
# ev_info.station = '*,-PARO' 
# 
# # event 3
# ev_info.network = '*,-PN,-CB,-SY,-XC'
# ev_info.station = '*,-H0160,-H0170,-H0180'
# 
# # event 4
# ev_info.network = '*,-PN,-SY'
# ev_info.station = '*'
# 
# # event 5
# ev_info.network = '*,-PN,-SY'
# ev_info.station = '*'

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
    iev_info.edep = line[3]*1000 # sac headers will be in km if using this correction -- my original depths are in km but the scripts expect meters.
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

