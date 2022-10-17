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
        ev_info.isave_raw = True
        ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = True

        # EVENT INFO
        # https://www.jordskjelv.no/jordskjelv/meldinger/jordskjelv-i-norskehavet-160-km-vest-for-forde-article4278-851.html
        # 2022-03-21 06:32, 61.4582, 2.4296, 4.7, 10 km
        # https://earthquake.usgs.gov/earthquakes/eventpage/us6000h6bi/origin/detail
        # 2022-03-21 05:32:53.604 UTC,  61.567°N  2.419°E, 10.0 km 
        # http://norsardata.no/NDC/bulletins/regional/2022/03/23540.html
        #     Origin time        Lat        Lon     Depth    Trms  Azrms  Nph  Nsta   Mag     Majax   Minax  Strike   Area
        # 2022-080:05.32.55.34  61.5584     2.3871  10.00    0.56 999.00   69   40    4.70      0.3     0.1  123.5      0.1 

        #-----------------------------------------------------------
        # the following otime was used for the DC moment tensor inversion.
        # keep for reference, but for the paper may need to finalize lon, lat, depth time.
        ev_info.otime = obspy.UTCDateTime("2022-03-21T05:32:57.008Z")   # 
        ev_info.elon = 2.4296
        ev_info.elat = 61.4582
        ev_info.edep = 1000
        ev_info.emag = 4.7
        #-----------------------------------------------------------

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000

        ev_info.network = 'GR'
        ev_info.network = 'KQ,TH,SX'
        #ev_info.channel = 'LH?,BH?,HH?,SH?'
        ev_info.channel = 'BH?,HH?'
        #ev_info.channel = 'HH?' # the DC solution used only HH stations
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
