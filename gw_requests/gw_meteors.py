#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
main resource:
https://cneos.jpl.nasa.gov/fireballs/

# The 2018 Qaanaaq Fireball
# (I found out about it by chance when looking for "greenland seismic stations"
https://agu.confex.com/agu/fm18/meetingapp.cgi/Paper/456944
http://adsabs.harvard.edu/abs/2018AGUFM.P21E3406S
https://cneos.jpl.nasa.gov/fireballs/


20190318 -- cralvizuri <celso.alvizuri@gmail.com>
"""


import obspy
import read_event_obspy_file as reof
from getwaveform import *


def get_ev_info(ev_info,iex):
    ev_info.idb = 1
    ev_info.use_catalog = 0
    ev_info.otime = obspy.UTCDateTime("2018-07-25T:21:55:26")
    ev_info.min_dist = 0 
    ev_info.max_dist = 2000
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 2000

    ev_info.ifFilter = True
    ev_info.ipre_filt = 2
    ev_info.filter_type = 'bandpass'
    ev_info.f1 = 1/1000  # fmin
    ev_info.f2 = 20      # fmax
    ev_info.corners = 4
    ev_info.remove_response = True
    ev_info.demean = True
    ev_info.detrend = True
    ev_info.output_cap_weight_file = True
    # ev_info.outformat = 'DISP'
    ev_info.ifsave_sacpaz = True
    ev_info.isave_raw = True
    #ev_info.ifverbose = False

    ev_info.network = '*'
    ev_info.channel = 'LH?,BH?,HH?'
    ev_info.use_catalog = 0
    ev_info.elat = 76.9
    ev_info.elon = -69.0
    ev_info.edep = -43300
    ev_info.emag = -999
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100
    ev_info.overwrite_ddir = 1

    return(ev_info)
