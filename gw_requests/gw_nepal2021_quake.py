import obspy
import read_event_obspy_file as reof
from getwaveform import *
import sys

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        ev_info.idb = 1            # 1: do not use massdownloader. add custom/manual clients.
        # DATA PREPARATION / PROCESSING
        ev_info.use_catalog = 0
        ev_info.ifmass_downloader = False
        #ev_info.iris_federator = True
        ev_info.ifverbose = True    # output all proccessing steps
        ev_info.overwrite_ddir = 0    # do NOT delete the existing directory + data

        #keep stations with missing components and fill the missing component with a null trace (MPEN)
        #Be sure to set the null component to 0 in the weight file when running cap
        #ev_info.icreateNull = 1
        ev_info.icreateNull = 1 # 2021-05-19 use, else removes all stations for raspberry shake

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        #ev_info.isave_raw = True
        #ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = False
        #ev_info.isave_ENZ = True

        # EVENT INFO
        # Shiba email 2021-05-19. Origin time: 2021-05-18T23:57:58 UTC (USGS)
        # https://earthquake.usgs.gov/earthquakes/eventpage/us7000e4aq/executive
	# Magnitud uncertainty  5.3 mb ± 0.0
	# Location uncertainty 28.281°N  84.330°E ± 7.6 km
	# Depth uncertainty     10.0 km ± 1.8
	# Origin Time 2021-05-18 23:57:58.791 UTC 
        ev_info.otime = obspy.UTCDateTime("2021-05-18T23:57:58.791")
        ev_info.elon = 84.330
        ev_info.elat = 28.281
        ev_info.edep = 10000
        ev_info.emag = 5.3

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1000

        #ev_info.network = 'ZB'
        ev_info.client_name = 'RASPISHAKE'
        ev_info.network = 'AM'
        #ev_info.station = 'RCCCC'  # for testing
        ev_info.channel = '*'
        ev_info.resample_TF = True
        ev_info.resample_freq = 20
        ev_info.scale_factor = 100
        #ev_info.phase_window = False
        #-------for specfem------------
        #ev_info.tbefore_sec = 0
        #ev_info.resample_TF = False
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        #------------------------------

    return(ev_info)
