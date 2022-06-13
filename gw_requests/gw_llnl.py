import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    #-----------------------------------------------------------
    # EVENT INFO
    ev_info.use_catalog = 0
    ## ev_info.resample_freq = 0  # no resampling
    ## ev_info.otime = obspy.UTCDateTime("1991-09-14T19:00:00.000Z")   # Hoya actual
    ev_info.otime = obspy.UTCDateTime("1991-09-14T19:00:08.031Z")   # Hoya target
    #ev_info.elon, ev_info.elat, ev_info.edep  = 9.60, 46.29, 0
    #ev_info.emag = 0

    ## NETWORK, STATIONS
    ev_info.idb = 3
    ev_info.network = '*'

    ev_info.station = '*'
    ev_info.channel = 'BH?,HH?,LH?'
    ev_info.overwrite_ddir = 0
    #-----------------------------------------------------------

    ev_info.min_dist = 0 
    ev_info.max_dist = 1200
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 600

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
    ev_info.ifverbose = False

    ev_info.use_catalog = 0
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100
    #ev_info.password = '895849_sed'
    #ev_info.password = '908588_geod_res'

    return(ev_info)
