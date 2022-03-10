import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        # DATA PREPARATION / PROCESSING
        ev_info.use_catalog = 0
        ev_info.idb = 1
        ev_info.ifmass_downloader = False
        ev_info.client_name = "NORSAR"
        #ev_info.iris_federator = True
        ev_info.ifverbose = True    # output all proccessing steps

        #keep stations with missing components and fill the missing component with a null trace (MPEN)
        #Be sure to set the null component to 0 in the weight file when running cap
        #ev_info.icreateNull = 1
        ev_info.icreateNull = 0

        ev_info.overwrite_ddir = 1 

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False

        # EVENT INFO
        # NK6m nk paper alvizuri-tape
        #  2017/09/03 03:38:31.8100  129.078  41.300
        #ev_info.otime = obspy.UTCDateTime("2017-09-03T03:38:31.8100")
        ev_info.otime = obspy.UTCDateTime("2017-09-03T03:30:01.760")
        ev_info.elon = 129.078
        ev_info.elat = 41.300
        ev_info.edep = 0
        ev_info.emag = 5.2

        ev_info.min_dist = 0
        ev_info.max_dist = 1000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

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
