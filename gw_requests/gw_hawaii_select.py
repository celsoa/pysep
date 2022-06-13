import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    if iex == 0:
        ev_info.idb = 1
        
        # https://earthquake.usgs.gov/earthquakes/eventpage/us70008jr5
        ev_info.use_catalog = 0
        # the following I filtered using seismicity 2017-1028
        # TRY1  2018-02-01T12:32:12.754000Z -155.28212          19.412129999999998 12.073 2.12 # I didn't see any signal for this event
        #ev_info.otime = obspy.UTCDateTime("2018-02-01T12:32:12.754000Z")
        #ev_info.elon = -155.28212
        #ev_info.elat = 19.412129999999998
        #ev_info.edep = 12073
        #ev_info.emag = 2.12
        ## TRY2  2018-06-28T05:23:04.240000Z -155.28481000000002 19.5055            11.48  3.36
        #ev_info.otime = obspy.UTCDateTime("2018-06-28T05:23:04.240000Z")
        #ev_info.elon = -155.28481000000002
        #ev_info.elat = 19.5055
        #ev_info.edep = 11480
        #ev_info.emag = 3.36
        # TRY3 2017-11-01T00:00:00.000000Z -155.280 19.409 12.1     ** extract 1-days worth of data, look for LP/VLP events **
        ev_info.otime = obspy.UTCDateTime("2017-11-01T00:00:00.000000Z")
        ev_info.elon = -155.280
        ev_info.elat = 19.409
        ev_info.edep = 12100
        ev_info.emag = 1.00

        ev_info.min_dist = 0 
        ev_info.max_dist = 600
        #ev_info.tbefore_sec = 100
        #ev_info.tafter_sec = 1000  
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 86400 * 5 + 100   
        ev_info.station = 'NPT,UWE,KKO,SDH,PAUD'
        ev_info.channel = 'HH?'
        ev_info.location = ''
        # NOTE ndays 2 works.
        # NOTE ndays 20 didn't work. error:
        # Apply instrument corrections
        # [2]    22029 floating point exception (core dumped)  python run_getwaveform.py gw_hawaii_select
        # python run_getwaveform.py gw_hawaii_select  1652.70s user 916.80s system 79% cpu 54:09.02 total


        ev_info.ifFilter = True
        ev_info.ipre_filt = 2
        ev_info.filter_type = 'bandpass'
        #ev_info.f1 = 1/1000  # orig
        ev_info.f1 = 1/2000  # try 2 (2020-02-04)
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

        #ev_info.network = '*,-PN,-XL,-6F'
        #ev_info.channel = 'LH?,BH?,HH?'
        ev_info.use_catalog = 0
        ev_info.resample_freq = 20
        ev_info.scale_factor = 100
        ev_info.overwrite_ddir = 1

    return(ev_info)
