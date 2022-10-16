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
        # Full list of icequakes since 2000: https://earthquake.usgs.gov/earthquakes/map/?currentFeatureId=us7000i3gd&extent=55.72092,219.47388&extent=59.79511,232.25098&range=search&sort=oldest&showUSFaults=true&baseLayer=terrain&timeZone=utc&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%222000-01-01%2000:00:00%22,%22endtime%22:%222022-10-16%2023:59:59%22,%22minmagnitude%22:2.5,%22eventtype%22:%22ice%20quake%22,%22orderby%22:%22time%22%7D%7D
        # Largest icequake in the list: M 3.4 Ice Quake - 93 km NW of Elfin Cove, Alaska
        # 2012-06-11 22:23:54 (UTC)58.862°N 137.323°W0.0 km depth
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak0127hxu5g3/executive
        ev_info.otime = obspy.UTCDateTime("2012-06-11T22:23:54")
        ev_info.elon = -137.323
        ev_info.elat = 58.862
        ev_info.edep = 0
        ev_info.emag = 3.4

        ev_info.min_dist = 0
        ev_info.max_dist = 500
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
        #ev_info.channel = '*H*' # DEFAULT. be sure to include SH for IMS data (vertical sensors)
        #                        # do not use '*' bc it finds BDF LDA data with no instrument response.
        ##ev_info.channel = 'BH*,HH*,SH*,MH*' # 2022-09-12 doesnt' work.
        #ev_info.icreateNull = 1 # NOTE USE. Else vertical-only stations will not be saved.
        ##-----------------------------------------------------------


    return(ev_info)
