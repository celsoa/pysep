import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    #-----------------------------------------------------------
    # EVENT INFO
    ev_info.use_catalog = 0
    # Bondo: /home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_ch2017_landslide.txt
    ev_info.otime = obspy.UTCDateTime("2017-08-23T07:30:00")
    ev_info.elon, ev_info.elat, ev_info.edep  = 9.60, 46.29, 0
    ev_info.emag = 0

    ## NETWORK, STATIONS
    ## 2019-07-31 For Bondo do the following:
    ## -- request Z3 (idb=1 or 5 works)
    ## -- request CH with idb=5 (idb=1 may cause some issues, see getwaveform.py
    ## -- request *  with idb=1
    ev_info.idb = 5; ev_info.network = 'Z3' # part 1
    #ev_info.idb = 5; ev_info.network = 'CH' # part 2
    #ev_info.idb = 1; ev_info.network = '*'  # part 3

    ev_info.station = '*'
    ev_info.channel = 'BH?,HH?,LH?'
    ev_info.overwrite_ddir = 0
    #-----------------------------------------------------------

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
    ev_info.ifsave_sacpaz = True
    ev_info.isave_raw_processed = True
    ev_info.ifverbose = False

    ev_info.use_catalog = 0
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100
    #ev_info.password = '895849_sed'
    #ev_info.password = '908588_geod_res'

    return(ev_info)
