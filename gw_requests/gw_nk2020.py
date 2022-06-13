import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    if iex == 0:
        ev_info.idb = 1
        ev_info.use_catalog = 0
        ev_info.otime = obspy.UTCDateTime("2020-05-11T10:45:06.0")
        ev_info.elon =127.14  
        ev_info.elat =38.72  
        ev_info.edep =10000 
        ev_info.emag =4

        ev_info.min_dist = 0 
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000  
        #ev_info.tbefore_sec = 100
        #ev_info.tafter_sec = 86400 * 5 + 100   
        ev_info.channel = 'HH?,BH?,LH?'
        ev_info.network = '*,-PN,-XL'
        ev_info.location = ''

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

        ev_info.use_catalog = 0
        ev_info.resample_freq = 20
        ev_info.scale_factor = 100
        ev_info.overwrite_ddir = 1

    return(ev_info)
