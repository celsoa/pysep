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

        # EVENT  21806005 NORTH KOREA
		#    Date       Time        Err   RMS Latitude Longitude  Smaj  Smin  Az Depth   Err Ndef Nsta Gap  mdist  Mdist Qual   Author      OrigID
		# 2022/02/18 11:17:53.65   1.99  0.76  40.4270  129.7810  58.6  32.7  11 600.0f         4    4 153   7.70  92.65 a i uk IDC_SEL3  21806007
        ev_info.otime = obspy.UTCDateTime("2022-02-18T11:17:53.650000Z")
        ev_info.elon = 129.7810
        ev_info.elat = 40.4270
        ev_info.edep = 600
        ev_info.emag = 4.5

        ev_info.min_dist = 0
        ev_info.max_dist = 1000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1000

        ev_info.channel = 'BH?,HH?'
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
