#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
Script to get waveform data for events at the Nevada Test Site. 
This data is for the following paper

C. Alvizuri, V. Silwal, L. Krischer, and C. Tape. Estimation of full moment
tensors with uncertainties, for earthquakes, volcanic events, and nuclear
tests. Geophysics (in prep.).

Data sources:
    LLNL
    IRIS
    NCEDC

Data references:
    Walter et al (2004) (LLNL dataset)
    Ford et al (2009)   (event selection)

This script is based on script run_getwaveform_fmtu2016.py

20170816 cralvizuri <celso.alvizuri@gmail.com>
"""

import obspy
from getwaveform import *
import util_helpers as uh
def get_ev_info(ev_info, iex):
    #from getwaveform import *
    # import sys
    # 
    def client2ev_info(iev_info, iclient):
        """
        call run_get_waveform
        """

        # prepare waveform requests
        # IRIS and BK
        iev_info.idb = 1
        if "IRIS" in iclient:
            print("Working data client", iclient, "event", iev_info.evname)
            iev_info.network = 'XP'
            iev_info.channel = 'HH?'
        elif "BK" in iclient:
            print("Working data client", iclient, "event", iev_info.evname)
            iev_info.network = 'BK'
            iev_info.station = '*'  # BK doesn't filter, use '*'
        elif "LLNL" in iclient:
            print("Working data client", iclient, "event", iev_info.evname)
            iev_info.idb = 3
            iev_info.station = '*'  # all stations
            iev_info.channel = '*'

        pass

    #events_file="/home/vipul/REPOSITORIES/manuscripts/alvizuri/papers/2016fmtu/data/event_info_llnl.txt"
    #events_file="here"
    events_file="/home/calvizur/REPOSITORIES/manuscripts-uaf/alvizuri/papers/2014fmt/data/uturuncu_mech.txt"
    skip_headers = 22   # starts at index = 0
    # KERNVILLE              , 1988-02-15T18:10:00.09, -116.472,  37.314,   542, Ford2009,      5.30, ml, NCSN 
    # AMARILLO               , 1989-06-27T15:30:00.02, -116.354,  37.275,   640, Ford2009,      4.90, ml, NCSN 
    # DISKO_ELM              , 1989-09-14T15:00:00.10, -116.164,  37.236,   261, Ford2009,      4.40, ml, NCSN 

    fid = open(events_file, "r")
    #data = fid.readlines()[0:iex]
    data = fid.readlines()[skip_headers:]
    fid.close()

    ev_info = getwaveform()
    ev_info.overwrite_ddir = 0
    ev_info.use_catalog = 0          # do not use event catalog for source parameters
    ev_info.min_dist = 0
    ev_info.max_dist = 1200
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 600
    ev_info.scale_factor = 100 
    ev_info.resample_TF = False
    ev_info.resample_freq = 20
    ev_info.f1 = 1/200  # fmin
    ev_info.f2 = 50  # fmax
    ev_info.ifsave_stationxml = False

    ev_info_list = []
    for row in data:
        iev_info = ev_info.copy()
        row_elements = row.split()
        eid = row_elements[-1]
        print("--------------> ", row_elements)
        print(type(eid))
        iev_info.otime = uh.eid2otime(eid)
        iev_info.elon = row_elements[6]
        iev_info.elat = row_elements[7]
        iev_info.edep = float(row_elements[8]) * 1000.0 # meters
        iev_info.emag = row_elements[16]

        # event objects for each event
        iev_info.evname = util_helpers.otime2eid(iev_info.otime)
        iev_info.get_events_client()

        client2ev_info(iev_info, 'IRIS'); ev_info_list.append(iev_info)

    return(ev_info_list)
