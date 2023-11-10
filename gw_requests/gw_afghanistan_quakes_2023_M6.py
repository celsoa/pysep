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

        #-----------------------------------------------------------
        # EVENT INFO
        #

        ## M 6.3 - 33 km NNE of Zindah Jān, Afghanistan -- MAIN/FIRST EVENT 
        ## https://earthquake.usgs.gov/earthquakes/eventpage/us6000ldpg/executive
        ## 2023-10-07 06:41:03.428 UTC, 34.610°N  61.924°E, 14.0 km, 6.3 mww 
        #ev_info.otime = obspy.UTCDateTime("2023-10-07T06:41:03.428Z")
        #ev_info.elon = 61.924
        #ev_info.elat = 34.610
        #ev_info.edep = 14000
        #ev_info.emag = 6.3

        ## M 6.3 - 29 km NNE of Zindah Jān, Afghanistan -- AFTERSHOCK #2 (m6.3)
        ## https://earthquake.usgs.gov/earthquakes/eventpage/us6000ldpm/executive
        ## 2023-10-07 07:12:50.042 UTC, 34.574°N  61.904°E, 10.0 km, mag 6.3 mww 
        #ev_info.otime = obspy.UTCDateTime("2023-10-07T07:12:50.042Z")
        #ev_info.elon = 61.904
        #ev_info.elat = 34.574
        #ev_info.edep = 10000
        #ev_info.emag = 6.3

        # M 6.3 - 30 km NNW of Herāt, Afghanistan -- AFTERSHOCK #3 (m6.3)
        # https://earthquake.usgs.gov/earthquakes/eventpage/us6000lfn5/origin/detail
        # 2023-10-15 03:36:00.037 UTC ,34.609°N  62.112°E, 6.3 km ,6.3 mww
        ev_info.otime = obspy.UTCDateTime("2023-10-15T03:36:00.037Z")
        ev_info.elon = 62.112
        ev_info.elat = 34.609
        ev_info.edep = 6300
        ev_info.emag = 6.3
        #-----------------------------------------------------------

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
