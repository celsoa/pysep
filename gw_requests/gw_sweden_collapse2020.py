import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        # DATA PREPARATION / PROCESSING
        ev_info.use_catalog = 0
        ev_info.ifmass_downloader = True
        #ev_info.iris_federator = True
        ev_info.idb = 1 # 1 IRIS
        ev_info.ifverbose = True    # output all proccessing steps

        #keep stations with missing components and fill the missing component with a null trace (MPEN)
        #Be sure to set the null component to 0 in the weight file when running cap
        #ev_info.icreateNull = 1
        ev_info.icreateNull = 0

        ev_info.overwrite_ddir = 0  

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False

        ## EVENT INFO USGS
        ## 67.826°N 20.267°E 1.0 km depth , https://earthquake.usgs.gov/earthquakes/eventpage/us70009ja2/technical
        #ev_info.otime = obspy.UTCDateTime("2020-05-18T01:11:56") # 2020-05-18 01:11:56
        #ev_info.elon = 20.267
        #ev_info.elat = 67.826
        #ev_info.edep = 1000
        #ev_info.emag = 4.9

        # EVENT INFO ISC -- http://www.isc.ac.uk/cgi-bin/wfreq/prepare?evid=618291845&schema=isc
        # ISC 	2020/05/18 01:11:55.328 	67.7951 	20.1931 	0.0
        ev_info.otime = obspy.UTCDateTime("2020-05-18T01:11:55.328") # obtained on 2022-08-31 13:38
        ev_info.elon = 20.1931
        ev_info.elat = 67.7951
        ev_info.edep = 0
        ev_info.emag = 4.7 # MW  4.7 GCMT -- from the link above 

        ev_info.min_dist = 0
        ev_info.max_dist = 1500
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 500

        ev_info.channel = 'BH?,HH?'
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
