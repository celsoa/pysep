#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
list of events for the himfmt project

20170816 -- calvizuri <celso.alvizuri@unil.ch>
"""

from getwaveform import *
import sys

events_file="/home/calvizur/REPOSITORIES/projects/himMT/data/test2.txt"
events_file="/home/calvizur/REPOSITORIES/projects/himMT/data/test3.txt"
events_file="/home/calvizur/REPOSITORIES/projects/himMT/data/bhutan2013.txt"
fid = open(events_file, "r")
data = fid.readlines()
fid.close()

ev_info = getwaveform()
ev_info.idb = 5
ev_info.ifsave_stationxml = False   # this causes errors so I disable for now
ev_info.overwrite_ddir = 0       # delete data dir if it exists
ev_info.use_catalog = 0          # do not use event catalog for source parameters
ev_info.min_dist = 0
ev_info.max_dist = 1000
ev_info.tbefore_sec = 100
ev_info.tafter_sec = 300
ev_info.network = 'XA' # IC XA YL are the only networks returned within a 1000-km radius, at least for the time of the main event
#ev_info.network = 'IC,XA,YL' # IC XA YL are the only networks returned within a 1000-km radius, at least for the time of the main event
# NOTE station PPWIN.PN is disabled since it's missing deconv info and it crashes the scripts (when doing a full-station search for available data)
# To see this add "print(station)" as line 238 in /home/calvizur/UTILS/anaconda3/envs/seis/lib/python3.6/site-packages/obspy/io/stationxml/core.py 
ev_info.station = '*'
ev_info.channel = 'HH?,BH?'
ev_info.scale_factor = 100 
ev_info.resample_TF = True
ev_info.resample_freq = 40
ev_info.user = 'bhutan1156arc'
ev_info.password = 'bhutan1156arc'

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

