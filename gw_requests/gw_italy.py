import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
# 
    if iex == 0:
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
        ####################
        #ev_info.otime = obspy.UTCDateTime("2018-11-18T12:48:46.3")  # M 4.2 - NORTHERN ITALY - 2018-11-18 12:48:46 UTC
        #ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 12.49, 44.07, 43, 4.2
        # from Laura Scognamiglio  catalog
        # % lon     lat     % depth Mw  strike1 dip1 rake1 strike2 dip2 rake2   m0 e0 quality % mxx mxy mxz myy myz mzz                               % id_event % date time
        # % 13.2623 42.5468 % 6     5.14 331    58   -91   153 32  -88  6.38513 23 Aa         % 859.783 4549.761 2752.311 2457.749 1441.783 -5409.544 % 39187681 % 2017/01/18 09:25:40.380
        ev_info.otime = obspy.UTCDateTime("2017-01-18T09:25:40.3")
        ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 13.2623, 42.5468, 6, 5.14
        ####################
        ev_info.resample_freq = 20
        # ev_info.rlat = 61.45420
        # ev_info.rlon = -149.7428
        # ev_info.rtime = obspy.UTCDateTime("2009-04-07T20:12:55.351")
        ev_info.network = 'IV,GU,IV,MN,NI,OX,RF,SI,ST,TV'  # try * for italy?
        ev_info.network = '*'
        ev_info.channel = 'BH?,LH?,HH?'
        ev_info.use_catalog = 0
        ev_info.idb = 1 
        ev_info.use_catalog = 0
        ev_info.min_dist = 0 
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000
        ev_info.scale_factor = 100

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
        ev_info.output_cap_weight_file = False
        # ev_info.outformat = 'DISP'
        ev_info.ifsave_sacpaz = True
        ev_info.overwrite_ddir = 0

        #ev_info.phase_window = False
        #-------for specfem------------
        #ev_info.tbefore_sec = 0
        #ev_info.resample_TF = False
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        #------------------------------

    return(ev_info)
#=================================================================================
# END EXAMPLES
#=================================================================================
