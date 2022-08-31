import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        # DATA PREPARATION / PROCESSING
        ev_info.idb = 1 # 1 = IRIS
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

        # EVENT: UA detections by VAKT
        #-----------------------------------------------------------
        # Largest COA: 2022-03-26T04:00:02.075000Z	29.629483	50.744524	172.4
        ev_info.otime = obspy.UTCDateTime("2022-03-26T04:00:02.075000Z")
        ev_info.elon = 29.629483
        ev_info.elat = 50.744524
        #-----------------------------------------------------------
        ## Ben's suggested event: 20220520053958800	2022-05-20T05:39:58.525000Z	29.283408	50.763136	17.76
        #ev_info.otime = obspy.UTCDateTime("2022-05-20T05:39:58.525000Z")
        #ev_info.elon = 29.283408
        #ev_info.elat = 50.763136
        #-----------------------------------------------------------
        # Largest Mag: 2022-02-25T08:32:40.775000Z	31.065704	52.021249
        ev_info.otime = obspy.UTCDateTime("2022-02-25T08:32:40.775000Z")
        ev_info.elon = 31.065704
        ev_info.elat = 52.021249
        #-----------------------------------------------------------
        ev_info.edep = 0
        ev_info.emag = -999

        ev_info.min_dist = 0
        ev_info.max_dist = 1000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1000

        ev_info.channel = 'SH?,LH?,BH?,HH?'
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

        # IMS DATA: ENABLE THE FOLLOWING TO GET IMS DATA
        ev_info.ifmass_downloader = False
        ev_info.client_name = 'IMS-SMP'
        #ev_info.station = 'USRK,KSRS,HILR,MJAR' # 2022-08-05 ISSUE: HILR returns empty
        ev_info.station = 'AKASG,GERES,KIV,FINES,BRMAR' # 2022-08-05 ISSUE: IM.GEA0..SHZ : Exception: No matching channel metadata found.
        ev_info.channel = '*'
        ev_info.channel = 'LH?,BH?,HH?'

    return(ev_info)
