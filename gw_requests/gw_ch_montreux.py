import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    #-----------------------------------------------------------
    # EVENT INFO
    ev_info.use_catalog = 0
    # widely felt in switzerland. montreaux!
    # http://www.seismo.ethz.ch/en/earthquakes/switzerland/eventpage.html?originId=%27c21pOmNoLmV0aHouc2VkL3NjM2Evb3JpZ2luL05MTC4yMDE5MDUyOTE1NTQwMS4yNzMzMDEuNDY3MzU=%27&date_ch=2019-05-28&time_ch=10:48&region=Montreux%20VD&magnitude=4.2
    ev_info.otime = obspy.UTCDateTime("2019-05-28T08:48:05")
    ev_info.elon = 6.745
    ev_info.elat = 46.373
    ev_info.edep = 4400
    ev_info.emag = 4.2

    # NETWORK, STATIONS
    #ev_info.idb = 1; ev_info.network = '*';  ev_info.station = '*'; ev_info.channel = 'BH?,LH?,HH?'
    ev_info.idb = 5; ev_info.network = 'CH'; ev_info.station = '*'; ev_info.channel = 'HH?'
    #-----------------------------------------------------------

    ev_info.min_dist = 0 
    ev_info.max_dist = 1000
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 1000

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
    ev_info.isave_raw = True
    ev_info.ifverbose = True

    ev_info.use_catalog = 0
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100
    ev_info.overwrite_ddir = 0

    return(ev_info)
