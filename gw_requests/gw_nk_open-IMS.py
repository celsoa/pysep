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
        # NK6. ISC: 2017-09-03T03:30:01.000Z  129.0801   41.2968  0.0    6.3
        # http://www.isc.ac.uk/cgi-bin/web-db-run?event_id=610943403&out_format=ISF2&request=COMPREHENSIVE&table_owner=gtdb
        #   ev_info.otime = obspy.UTCDateTime("2017-09-03T03:30:01.000Z")
        #   ev_info.elon = 129.0801
        #   ev_info.elat = 41.2968
        #   ev_info.edep = 0
        #   ev_info.emag = 6.3

        # NK PAPER. NK6 main
        # 2017-09-03T03:30:01.760000Z     129.0297000     41.3324000       0.0     6.3 | us        361       10.0      3.309     
        ev_info.otime = obspy.UTCDateTime("2017-09-03T03:30:01.760000Z")
        ev_info.elon = 129.0297000
        ev_info.elat = 41.3324000
        ev_info.edep = 1
        ev_info.emag = 6.3
        #-----------------------------------------------------------

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.channel = 'BH?,HH?,EH?'
        #ev_info.exclude_net = 'BK,NO,NS'
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

        #-----------------------------------------------------------
        # IMS REQUEST
        # Be sure to specify each IMS station. wildcard '*' is not implemented.
        ev_info.idb = 0
        ev_info.ifmass_downloader = False
        ev_info.client_name = 'IMS-SMP'
        #ev_info.station = 'FINES'
        #ev_info.station = 'I37NO'
        ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
                                # do not use '*' bc it finds BDF LDA data with no instrument response.
        #ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        ev_info.icreateNull = 1 # NOTE USE. Else vertical-only stations will not be saved.
        #-----------------------------------------------------------


    return(ev_info)
