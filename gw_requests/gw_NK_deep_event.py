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

        # EVENT INFO -- CTBTO IDC PRODUCT
        # Distance from  North Korea ( 41.3, 129.1 ):  82.4594 km ======================================================================
        # EVENT  24655033 NORTH KOREA
        # Date       Time          Err   RMS   Latitude Longitude  Smaj  Smin  Az  Depth   Err Ndef Nsta Gap  mdist  Mdist Qual   Author      OrigID
        # 2023/09/06 15:52:15.31   0.75  4.20  41.4679  130.0603   10.2   9.6  124 636.2  10.7   45   45  55   3.07 141.97 a i uk IDC_SEL3  24656144
        # Magnitude  Err Nsta Author      OrigID
        # mb     3.9 0.4   34 IDC_SEL3  24656144
        ev_info.otime = obspy.UTCDateTime("2023-09-06T15:52:15.31Z")
        ev_info.elon = 130.0603
        ev_info.elat = 41.4679
        ev_info.edep = 636.2*1000
        ev_info.emag = 3.9

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.channel = 'HH?,BH?'
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
