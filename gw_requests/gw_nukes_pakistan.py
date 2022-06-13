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
        ev_info.isave_raw = True
        ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = True

        # EVENT INFO
        # 1998-05-30T06:54:54.940Z 28.493 63.731 0 4.6  79  km  SW  of  Dalbandin,  Pakistan 
        # 1998-05-28T10:16:15.230Z 28.902 64.789 0 4.8  37  km  E  of  Dalbandin,  Pakistan 
        ev_info.otime = obspy.UTCDateTime("1998-05-30T06:54:54.940Z")
        ev_info.elon = 63.731
        ev_info.elat = 28.493
        ev_info.edep = 0
        ev_info.emag = 4.6
        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

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

    if iex == 1:
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
        ev_info.isave_raw = True
        ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = True

        # EVENT INFO
        # 1998-05-30T06:54:54.940Z 28.493 63.731 0 4.6  79  km  SW  of  Dalbandin,  Pakistan 
        # 1998-05-28T10:16:15.230Z 28.902 64.789 0 4.8  37  km  E  of  Dalbandin,  Pakistan 
        ev_info.otime = obspy.UTCDateTime("1998-05-28T10:16:15.230Z")
        ev_info.elon = 64.789
        ev_info.elat = 28.902
        ev_info.edep = 0
        ev_info.emag = 4.8
        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

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
    return(ev_info)
