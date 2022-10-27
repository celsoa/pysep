import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
# ===============================================================
# Full list of icequakes since 2000. USGS catalog (derived from Alaska catalog)
# https://earthquake.usgs.gov/earthquakes/map/?currentFeatureId=us7000i3gd&extent=55.72092,219.47388&extent=59.79511,232.25098&range=search&sort=oldest&showUSFaults=true&baseLayer=terrain&timeZone=utc&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%222000-01-01%2000:00:00%22,%22endtime%22:%222022-10-16%2023:59:59%22,%22minmagnitude%22:2.5,%22eventtype%22:%22ice%20quake%22,%22orderby%22:%22time%22%7D%7D
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
        # Largest icequake in the list: M 3.4 Ice Quake - 93 km NW of Elfin Cove, Alaska
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak0127hxu5g3/executive
        # Largest of the icequakes. great signal. FMTU shows localized-ish collapse
        # 2012-06-11T22:23:54.116000Z     -137.323      58.8616            0        3.4 | ice quake None | 93 km NW of Elfin Cove, Alaska
        ev_info.otime = obspy.UTCDateTime("2012-06-11T22:23:54")
        ev_info.elon = -137.323
        ev_info.elat = 58.862
        ev_info.edep = 0
        ev_info.emag = 3.4

        # SMALLER EVENT, EPICENTER IN THE OCEAN, DEPTH 1KM, BUT CLOSE TO A GLACIER TERMINUS. WHAT IS IT? Plus it's a M2.8 -- relatively larger.
        # NB: there is a signal in many stations, but this event looks too noisy.
        # https://earthquake.usgs.gov/earthquakes/eventpage/us7000354q/map
        # 2019-04-12T18:48:56.004000Z     -137.209      58.4352         1000        2.8 | ice quake None | 57 km WNW of Elfin Cove, Alaska
        ev_info.otime = obspy.UTCDateTime("2019-04-12T18:48:56.004000Z")
        ev_info.elon = -137.209
        ev_info.elat = 58.4352
        ev_info.edep = 1
        ev_info.emag = 2.8

        # EPICENTER NEAR TERMINUS
        # NB: there is some signal there, clearer about 1-3Hz, and I might be able to get a solution after carefully aligning traces.
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak0194df40bs/executive
        # 2019-04-05T18:56:53.673000Z     -137.266      58.4813            0        2.4 | ice quake None | 62 km WNW of Elfin Cove, Alaska
        ev_info.otime = obspy.UTCDateTime("2019-04-05T18:56:53.673000Z")
        ev_info.elon = -137.266
        ev_info.elat = 58.4813
        ev_info.edep = 0
        ev_info.emag = 2.4
        
        # SMALLER EVENT, EPICENTER ON GLACIER
        # Noisier signal and might be a little challenging but could stretch to get a solution
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak0196999c0p/executive
        # 2019-05-16T20:44:14.885000Z     -139.388      60.0013            0        1.7 | ice quake None | 54 km NNE of Yakutat, Alaska
        ev_info.otime = obspy.UTCDateTime("2019-05-16T20:44:14.885000Z")
        ev_info.elon = -139.388
        ev_info.elat = 60.0013
        ev_info.edep = 0
        ev_info.emag = 1.7

        # SMALLER EVENT, EPICENTER ON GLACIER
        # Signal is clearer between (1)2-5 Hz, clear onsets so might be able to model the first arrivals
        # yes, try FMT analysis with this event
        # aerial view of the glacier shows lots of sinuosity and twisted molasses/toffy looking paths.
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak0193jkcjyu
        # 2019-03-18T13:38:23.065000Z      -140.21      59.9007            0        2.2 | ice quake None | 47 km NW of Yakutat, Alaska
        ev_info.otime = obspy.UTCDateTime("2019-03-18T13:38:23.065000Z")
        ev_info.elon = -140.21
        ev_info.elat = 59.9007
        ev_info.edep = 0
        ev_info.emag = 2.2


#-----------------------------------------------------------
        # FOCUS: NEAR WRIGHT GLACIER CLUSTER PER NATALIA RUPPERT'S SUGGESTION.
        # I'M WORKING BACKWARDS FROM LARGEST TO SMALLEST
        # https://earthquake.usgs.gov/earthquakes/eventpage/us6000ibz0/ 
        # M 3.2 Ice Quake - 55 km E of Juneau, Alaska
        # 2022-08-18 21:48:22 (UTC)58.339°N 133.482°W1.0 km depth
        # 2022-08-18 21:48:22.000 UTC, 58.339°N  133.482°W
        # This one is near a terminus but close to a mountain so it could be either slump or break.
        # No signals below 0.5 Hz, so not a good candidate unless near stations.
        ev_info.otime = obspy.UTCDateTime("2022-08-18T21:48:22.000Z")
        ev_info.elon = -133.482
        ev_info.elat = 58.339
        ev_info.edep = 1000
        ev_info.emag = 3.2

        # Focus: near Wright glacier cluster per Natalia Ruppert's suggestion.
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak016gry1a9s/
        # M 3.4 Ice Quake - 45 km NNW of Juneau, Alaska
        # 2016-12-30 18:27:10 (UTC)58.672°N 134.769°W0.3 km depth
        # 2016-12-30 18:27:10.406 UTC, 58.672°N  134.769°W
        # there is a signal about 0.02 Hz but noise levels are a little high.
        # I might be able to do an inversion with some effort aligning signals.
        ev_info.otime = obspy.UTCDateTime("2016-12-30T18:27:10.406")
        ev_info.elon = -134.769
        ev_info.elat = 58.672
        ev_info.edep = 300
        ev_info.emag = 3.4

        # Focus: near Wright glacier cluster per Natalia Ruppert's suggestion.
        # https://earthquake.usgs.gov/earthquakes/eventpage/ak014dgx3mck/executive
        # M 3.2 Ice Quake - 38 km ESE of Hobart Bay, Alaska
        # 2014-10-20 21:22:54 (UTC)57.321°N 132.779°W0.0 km depth
        # 2014-10-20 21:22:54.447 UTC ,      57.321°N  132.779°W
        ev_info.otime = obspy.UTCDateTime("2014-10-20T21:22:54.447")
        ev_info.elon = -132.779
        ev_info.elat = 57.321
        ev_info.edep = 0
        ev_info.emag = 3.2


#-----------------------------------------------------------
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
