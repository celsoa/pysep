import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        # DATA PREPARATION / PROCESSING
        ev_info.idb = 1     # 1 = IRIS. % 20220223 calvizuri -- seems needed. not sure why I removed it previously. TODO revise conditional tests in getwaveform to deprecate this, if that's the goal
        ev_info.use_catalog = 0
        ev_info.ifmass_downloader = True
        #ev_info.iris_federator = True
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

        # EVENT INFO
        # https://earthquake.usgs.gov/earthquakes/eventpage/us2000a0jb/executive
        # M 4.1 - 150 km SSW of Turpan, China
        # 2017-07-24 21:46:39 (UTC)41.717°N 88.419°E    35.2 km depth
        ev_info.otime = obspy.UTCDateTime("2017-07-24T21:46:39.000Z")
        ev_info.elon = 88.419
        ev_info.elat = 41.717
        ev_info.edep = 35200
        ev_info.emag = 4.1

        ev_info.min_dist = 0
        ev_info.max_dist = 3000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1000

        ev_info.channel = 'LH?,BH?,HH?'
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
