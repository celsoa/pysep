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
        ev_info.ifverbose = True    # output all proccessing steps

        #keep stations with missing components and fill the missing component with a null trace (MPEN)
        #Be sure to set the null component to 0 in the weight file when running cap
        #ev_info.icreateNull = 1
        ev_info.icreateNull = 0

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        #ev_info.isave_raw = True
        #ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = False
        #ev_info.isave_ENZ = True

        # EVENT INFO
        # landslide India
        # 2017-02-07 04:51:14 (EGU21 16593)
        # 79.731631,  30.375864 (email Shobhana Lakhera, Michel Jaboy.)
        ev_info.otime = obspy.UTCDateTime("2021-02-07T04:51:14.000Z")
        ev_info.elon = 79.731631
        ev_info.elat = 30.375864
        ev_info.edep = -5413
        ev_info.emag = 4

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.channel = 'LH?,BH?,HH?'
        ev_info.resample_freq = 50
        ev_info.scale_factor = 100
        #ev_info.phase_window = False
        #-------for specfem------------
        #ev_info.tbefore_sec = 0
        #ev_info.resample_TF = False
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        #------------------------------


    return(ev_info)
