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

        ev_info.overwrite_ddir = 0  

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False

        # EVENT INFO
        # gw_AK_mag8_20210729.py
        # 2021-07-29T06:15:47.536000Z  -157.8414    55.3248       32200.0 8.2
        ev_info.otime = obspy.UTCDateTime("2021-07-29T06:15:47.536000Z")
        ev_info.elon = -157.8414
        ev_info.elat = 55.3248
        ev_info.edep = 32200.0
        ev_info.emag = 8.2

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1800

        #ev_info.channel = 'BH?'
        ev_info.channel = 'HH?'
        ev_info.resample_TF = True
        ev_info.resample_freq = 20 # ORIGINAL
        #ev_info.resample_freq = 50  # to match UAF greens
        ev_info.scale_factor = 100
        #ev_info.phase_window = False
        #-------for specfem------------
        #ev_info.tbefore_sec = 0
        #ev_info.resample_TF = False
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        #------------------------------


    return(ev_info)
