import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        # DATA PREPARATION / PROCESSING
        ev_info.idb = 1     # 1 = IRIS. % 20220223 calvizuri -- needed. not sure why I removed it previously. keep an eye.
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
        # 2022-02-26T08:12:27 (approx) - rocket strike (CCTV footage) https://en.wikipedia.org/wiki/Battle_of_Kyiv_(2022)
        # KYIV: lon 30.523333, lat 50.45
        # https://geohack.toolforge.org/geohack.php?pagename=Kyiv&params=50_27_00_N_30_31_24_E_region:UA_type:city
        #ev_info.otime = obspy.UTCDateTime("2022-02-21T00:00:00.000000Z")
        #ev_info.otime = obspy.UTCDateTime("2022-02-22T00:00:00.000000Z")
        #ev_info.otime = obspy.UTCDateTime("2022-02-23T00:00:00.000000Z")
        #ev_info.otime = obspy.UTCDateTime("2022-02-24T00:00:00.000000Z")
        #ev_info.otime = obspy.UTCDateTime("2022-02-25T00:00:00.000000Z")
        #ev_info.otime = obspy.UTCDateTime("2022-02-26T00:00:00.000000Z")
        #ev_info.otime = obspy.UTCDateTime("2022-02-27T00:00:00.000000Z")
        ev_info.otime = obspy.UTCDateTime("2022-02-28T00:00:00.000000Z")
        ev_info.elon = 30.523333
        ev_info.elat = 50.45 
        ev_info.edep = 0 
        ev_info.emag = 0

        ev_info.min_dist = 0
        #ev_info.max_dist = 1000
        ev_info.max_dist = 500
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 60 * 60 * 24

        ev_info.channel = 'BH?,HH'
        #ev_info.network = 'MD'
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
