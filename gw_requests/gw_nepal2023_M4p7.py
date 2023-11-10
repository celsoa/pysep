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
        # 2023-11-03 18:02:54.099 UTC 
        # 28.848°N  82.187°E
        # 16.5 km , Magnitude 5.7 mww 
        ev_info.otime = obspy.UTCDateTime("2023-11-03T18:02:54.099")
        ev_info.elon = 82.187
        ev_info.elat = 28.848
        ev_info.edep = 16500
        ev_info.emag = 5.7

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.channel = 'BH?,HH?'
        ev_info.resample_TF = True
        ev_info.resample_freq = 20
        ev_info.scale_factor = 100
        #ev_info.phase_window = False

        ##-----------------------------------------------------------
        ## SPECFEM  (NB 2023-07-21: LEGACY. HOW DOES IT WORK.
        ##-----------------------------------------------------------
        #ev_info.tbefore_sec = 0
        #ev_info.resample_TF = False
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        ##-----------------------------------------------------------

        ##-----------------------------------------------------------
        ## UIB-NORSAR REQUEST
        ## 2023-07-21 needed since UIB etc no longer support MASS_DOWNLOADER.
        ## USE GIT BRANCH: feature/imsdata, CONDA ENV: seismonpy_dev
        ##-----------------------------------------------------------
        #ev_info.client_name = "UIB-NORSAR" 
        #ev_info.ifmass_downloader = False

        ##-----------------------------------------------------------
        ## RASPISHAKE
        ## 2023-11-06 doesnt work --  obspy.clients.fdsn.header.FDSNNoDataException: No data available for request. HTTP Status code: 204
        ##-----------------------------------------------------------
        #ev_info.client_name = 'RASPISHAKE'
        #ev_info.network = 'AM'
        #ev_info.ifmass_downloader = False

        #-----------------------------------------------------------
        # IMS REQUEST
        # Be sure to specify each IMS station. wildcard '*' is not implemented.
        #-----------------------------------------------------------
        ev_info.idb = 0
        ev_info.ifmass_downloader = False
        ev_info.client_name = 'IMS-SMP'
        #ev_info.station = 'FINES'
        #ev_info.station = 'I37NO'
        ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
                                # do not use '*' bc it finds BDF LDA data with no instrument response.
        #ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        ev_info.icreateNull = 1 # NOTE USE. Else vertical-only stations will not be saved.

        ##-----------------------------------------------------------
        ## LOCAL DATA REPOSITORY, e.g. for data from Swedish Network
        ## NOTE: currently set only for Kiruna and NW Russia events.
        ##-----------------------------------------------------------
        #ev_info.idb = 0
        #ev_info.ifmass_downloader = False
        #ev_info.client_name = 'local'

    return(ev_info)
