import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    #-----------------------------------------------------------
    # EVENT INFO
    ev_info.use_catalog = 0
    # Bondo: /home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_ch2017_landslide.txt
    #ev_info.otime = obspy.UTCDateTime("2017-08-23T07:30:00")
    #ev_info.elon, ev_info.elat, ev_info.edep  = 9.60, 46.29, 0

    ## Taan Fjord. Event time and coords from Gualtieri 2017 
    ## event location and time NOT available at USGS or GCMT
    #ev_info.otime = obspy.UTCDateTime("2015-10-18T05:18:00")
    #ev_info.elon, ev_info.elat, ev_info.edep  = -141.187, 60.175, 0
    #ev_info.emag = 0

    #Lamplugh Glacier rock avalanche (the lituya event that I analyzed, I think)
    #https://earthquake.usgs.gov/earthquakes/eventpage/ak01689yds4l/executive
    #https://blogs.agu.org/landslideblog/2016/07/03/lamplugh-glacier-rock-avalanche-1/
    # https://www.adn.com/alaska-news/2016/07/02/massive-landslide-crashes-onto-glacier-in-southeast-alaska/
    ev_info.otime = obspy.UTCDateTime("2016-06-28T16:20:41")    # 2016-06-28 16:20:41
    ev_info.elon, ev_info.elat, ev_info.edep  = -136.907, 58.714, 0
    ev_info.emag = 0

    # NETWORK, STATIONS
    ev_info.idb = 1
    ev_info.network = '*'
    #ev_info.network = 'CH'
    #ev_info.network = 'Z3'
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
