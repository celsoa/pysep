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
        ev_info.idb = 1 # 1 IRIS
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

        ## EVENT INFO USGS
        # ISC: http://www.isc.ac.uk/cgi-bin/web-db-run?event_id=622117251&out_format=ISF2&request=COMPREHENSIVE
        # ISC, UPPSALA: 2022/03/05 00:13:26.10   2.50 0.500  67.6150   34.0440  0.13   0.5  -1   0.1f             11                       se UPP         616546394
        ev_info.otime = obspy.UTCDateTime("2022-03-05T00:13:26.1000") # obtained 2022-09-05 
        ev_info.elon = 34.0440
        ev_info.elat = 67.6150
        ev_info.edep = 0
        ev_info.emag = 3.1 # ML     3.1          UPP         616546394

        ev_info.min_dist = 1500
        ev_info.max_dist = 2200
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

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
        #ev_info.station = 'HFS' # 2022-09-23 NOTE mismatch channel metadata. HH EH
        ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
                                # do not use '*' bc it finds BDF LDA data with no instrument response.
        #ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        ev_info.icreateNull = 1 # NOTE USE. Else vertical-components will not be saved.
        #-----------------------------------------------------------


    return(ev_info)
