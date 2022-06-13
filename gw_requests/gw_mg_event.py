import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    ev_info.idb = 1
    ev_info.use_catalog = 0
    ev_info.otime = obspy.UTCDateTime("2018-11-11 09:31:52.0")  # GCMT
    #ev_info.otime = obspy.UTCDateTime("2018-11-11 09:31:00.0")  # try2: use slightly earlier time. ABPO arrivals are a little too early -- NB yeah but this changes otime, so best to use longer tbefore_sec
    # https://twitter.com/seismo_steve/status/1062007589767131136
    # https://pbs.twimg.com/media/Dr0B-hXXgAAfNOa.jpg # GCMT details for that day!
    ev_info.min_dist = 0 
    ev_info.max_dist = 2000
    #ev_info.tbefore_sec = 100   # orig
    ev_info.tbefore_sec = 300   # try3
    ev_info.tafter_sec = 3000

    ev_info.ifFilter = True
    ev_info.ipre_filt = 2
    ev_info.filter_type = 'bandpass'
    ev_info.f1 = 1/1000  # fmin
    ev_info.f2 = 10      # fmax
    ev_info.corners = 4
    ev_info.remove_response = True
    ev_info.demean = True
    ev_info.detrend = True
    ev_info.output_cap_weight_file = True
    ev_info.ifsave_sacpaz = True
    ev_info.isave_raw_processed = True
    ev_info.ifverbose = True

    ev_info.network = '*'
    ev_info.network = '*,-PN,-XL,-6F'
    #ev_info.channel = 'BH?,HH?,HN?,EH?'
    ev_info.channel = 'LH?,BH?,HH?'
    ev_info.station = '*,-WAID'
    #ev_info.station = '*'
    ev_info.use_catalog = 0
    #ev_info.elat = 45.25   # OLD (wrong!)
    #ev_info.elon = -12.75  # OLD (wrong!)
    ev_info.elon = 45.25
    ev_info.elat = -12.75
    ev_info.edep = 33
    ev_info.emag = 5
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100
    ev_info.overwrite_ddir = 1

    return(ev_info)
