import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
# SilwalTape2016 example event (Anchorage)
    if iex == 0:
        ev_info.idb = 1     # 4 --> ETH
        ev_info.use_catalog = 0
        ev_info.otime = obspy.UTCDateTime("2017-06-17T23:39:12")
        ev_info.min_dist = 0 
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        #ev_info.min_lat = 59
        #ev_info.max_lat = 62
        #ev_info.min_lon = -152
        #ev_info.max_lon = -147

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
        ev_info.isave_raw_processed = True
        ev_info.ifverbose = True

        # default list of Alaska networks
        # note 1: cannot use '*' because of IM
        # note 2: may want to exclude the mid-band AV network
        # note 3: these are temporary:
        # XE BEAAR 1999
        # XR ARCTIC 2004
        # XZ STEEP 2005
        # YV MOOS 2006
        # XV FLATS 2014
        # ZE SALMON 2015
        # XG WVF 2016
        # [7C MMEP 2015]
        # TA
        #ev_info.network = 'AK,AT,AV,CN,II,IU,US,XM,XV,XZ,YV'
        #ev_info.network = 'AK' # for testing
        #ev_info.network = 'AK,AT,AV,CN,II,IU,US,XM,TA,XE,XR,XZ,YV,XV,ZE,XG'
        #ev_info.station = 'KULLO'
        ev_info.network = '*'
        ev_info.channel = 'BH?,HH?'
        ev_info.use_catalog = 0
        ev_info.elat = 71.640
        ev_info.elon = -52.344
        ev_info.edep = 0
        # ev_info.rlat = 61.45420
        # ev_info.rlon = -149.7428
        # ev_info.rtime = obspy.UTCDateTime("2009-04-07T20:12:55.351")
        ev_info.emag = 4.2
        #ev_info.resample_TF = False
        ev_info.resample_freq = 20
        ev_info.scale_factor = 100
        #ev_info.phase_window = False
        ev_info.overwrite_ddir = 1
        #-------for specfem------------
        #ev_info.tbefore_sec = 0
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        #------------------------------

    return(ev_info)
#=================================================================================
# END EXAMPLES
#=================================================================================
