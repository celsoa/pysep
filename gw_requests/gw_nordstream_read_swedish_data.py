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
        ev_info.isave_raw = True
        ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = True

        ### EVENT INFO NORSAR
        ### http://www.norsardata.no/NDC/bulletins/alert/FIN/2022-269:17.05.20.6.html
        #ev_info.otime = obspy.UTCDateTime("2022-09-26T17:03:00.00") # obtained 2022-09-27
        #ev_info.elon = 16.154000
        #ev_info.elat = 55.262000
        #ev_info.edep = 0
        #ev_info.emag = 0

        ## EVENT 1
        ## from Ben, teams chat 2022-09-28 3:48 pm
        ## 00:03:24 (UTC) 54.765N 15.433E Magnitude 1.8 -- the location is from SNSN 
        #ev_info.otime = obspy.UTCDateTime("2022-09-26T00:03:24.00") # obtained 2022-09-27
        #ev_info.elon = 15.433
        #ev_info.elat = 54.765
        #ev_info.edep = 0
        #ev_info.emag = 1.8

        # EVENT 2
        # from Ben, teams chat 2022-09-28 3:48 pm
        # 17:03:50 (UTC) 55.59N 15.72E Magnitude 2.3
        ev_info.otime = obspy.UTCDateTime("2022-09-26T17:03:50.000") #
        ev_info.elon = 15.72
        ev_info.elat = 55.59
        ev_info.edep = 0
        ev_info.emag = 2.3

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

        ##-----------------------------------------------------------
        ## IMS REQUEST
        ## Be sure to specify each IMS station. wildcard '*' is not implemented.
        #ev_info.idb = 0
        #ev_info.ifmass_downloader = False
        #ev_info.client_name = 'IMS-SMP'
        ##ev_info.station = 'FINES'
        ##ev_info.station = 'I37NO'
        ##ev_info.station = 'HFS' # 2022-09-23 NOTE mismatch channel metadata. HH EH
        #ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
        #                        # do not use '*' bc it finds BDF LDA data with no instrument response.
        ##ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        #ev_info.icreateNull = 1 # NOTE USE. Else vertical-components will not be saved.
        ##-----------------------------------------------------------

        #-----------------------------------------------------------
        # LOCAL DATA REPOSITORY
        #-----------------------------------------------------------
        ev_info.idb = 0
        ev_info.ifmass_downloader = False
        ev_info.client_name = 'local'

    return(ev_info)
