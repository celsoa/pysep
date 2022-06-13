import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
# SilwalTape2016 example event (Anchorage)
    if iex == 0:
        ev_info.idb = 1     # 4 --> ETH
        ev_info.min_dist = 0 
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 600

        #ev_info.min_lat = 59
        #ev_info.max_lat = 62
        #ev_info.min_lon = -152
        #ev_info.max_lon = -147

        ev_info.ipre_filt = 1
        ev_info.filter_type = 'bandpass'
        ev_info.f1 = 1/1000  # fmin
        ev_info.f2 = 40      # fmax
        ev_info.corners = 4
        ev_info.remove_response = True
        ev_info.demean = True
        ev_info.detrend = True
        ev_info.output_cap_weight_file = True
        # ev_info.outformat = 'DISP'
        ev_info.ifsave_sacpaz = False

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
        ev_info.network = '*'

        ev_info.channel = 'BH?'
        ev_info.use_catalog = 0
        ev_info.use_catalog = 0
        ## 20011202132111740
        ## 20020203074158870
        # 20020326121014990 -- better snr
        # 20020502173530860 -- better snr
        # 20020913203502000 -- better snr
        ev_info.otime = obspy.UTCDateTime("2001-12-02T13:21:11.740000Z");  ev_info.elat = 28.448000; ev_info.elon = 87.226667; ev_info.edep = 1488; ev_info.emag = 3.62
        ev_info.otime = obspy.UTCDateTime("2002-02-03T07:41:58.870000Z");  ev_info.elat = 27.758667; ev_info.elon = 86.398833; ev_info.edep = 1990; ev_info.emag = 3.79
        ev_info.otime = obspy.UTCDateTime("2002-03-26T12:10:14.990000Z");  ev_info.elat = 28.063000; ev_info.elon = 87.458333; ev_info.edep = 4377; ev_info.emag = 3.37
        ev_info.otime = obspy.UTCDateTime("2002-05-02T17:35:30.860000Z");  ev_info.elat = 27.712167; ev_info.elon = 86.755167; ev_info.edep = 2574; ev_info.emag = 4.20
        ev_info.otime = obspy.UTCDateTime("2002-09-13T20:35:02.000000Z");  ev_info.elat = 27.502333; ev_info.elon = 87.305833; ev_info.edep = 1874; ev_info.emag = 3.19

        # ev_info.rlat = 61.45420
        # ev_info.rlon = -149.7428
        # ev_info.rtime = obspy.UTCDateTime("2009-04-07T20:12:55.351")
        ev_info.resample_freq = 40
        ev_info.scale_factor = 100
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
