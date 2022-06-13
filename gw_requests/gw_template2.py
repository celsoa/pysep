import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    #-----------------------------------------------------------
    # EVENT INFO
    ev_info.use_catalog = 0
    ev_info.otime = obspy.UTCDateTime("2017-01-24 09:50:30.8")
    ev_info.elat = 46.151
    ev_info.elon = 6.194
    ev_info.edep = 0
    ev_info.emag = 0

    # NETWORK, STATIONS
    ev_info.idb = 1
    #ev_info.network = '*'
    ev_info.network = 'CH'
    ev_info.channel = 'BH?,HH?'
    #-----------------------------------------------------------

    ev_info.min_dist = 0 
    ev_info.max_dist = 200
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
    ev_info.ifsave_sacpaz = True
    ev_info.isave_raw_processed = True
    ev_info.ifverbose = True

    ev_info.use_catalog = 0
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100
    ev_info.overwrite_ddir = 1

    return(ev_info)
