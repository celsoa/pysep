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

        # EVENT INFO -- random pick from the Balapan catalog. Test to see about data availability.
        # M 5.9 Nuclear Explosion - 99 km S of Kurchatov, Kazakhstan
        # 1985-02-10 03:27:07 (UTC)49.877°N 78.816°E0.0 km depth
        # https://earthquake.usgs.gov/earthquakes/eventpage/usp0002bs3/executive
        # EXAMPLE RESULT: [2022-10-26 08:51:07,918] - obspy.clients.fdsn.mass_downloader - INFO: Client 'IRIS' - No data available for request.
        ev_info.otime = obspy.UTCDateTime("1985-02-10T03:27:07.620Z")
        ev_info.elon = 78.816
        ev_info.elat = 49.877
        ev_info.edep = 0
        ev_info.emag = 5.9

        ev_info.min_dist = 0
        ev_info.max_dist = 3000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.channel = 'BH?,LH?,HH?,SH?,EH?'
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

        ##-----------------------------------------------------------
        ## IMS REQUEST
        ## Be sure to specify each IMS station. wildcard '*' is not implemented.
        #ev_info.idb = 0
        #ev_info.ifmass_downloader = False
        #ev_info.client_name = 'IMS-SMP'
        ##ev_info.station = 'FINES'
        ##ev_info.station = 'I37NO'
        #ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
        #                        # do not use '*' bc it finds BDF LDA data with no instrument response.
        ##ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        #ev_info.icreateNull = 1 # NOTE USE. Else vertical-only stations will not be saved.
        ##-----------------------------------------------------------


    return(ev_info)