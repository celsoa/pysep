import obspy
import read_event_obspy_file as reof
from getwaveform import *
import sys

def get_ev_info(ev_info,iex):
# ===============================================================
    if iex == 0:
        ev_info.overwrite_ddir = 0
        # DATA PREPARATION / PROCESSING
        ev_info.use_catalog = 0
        ev_info.ifmass_downloader = True
        #ev_info.iris_federator = True
        ev_info.ifverbose = True    # output all proccessing steps

        #keep stations with missing components and fill the missing component with a null trace (MPEN)
        #Be sure to set the null component to 0 in the weight file when running cap
        #ev_info.icreateNull = 1
        ev_info.icreateNull = 0

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        #ev_info.isave_raw = True
        #ev_info.isave_raw_processed = True
        ev_info.isave_ENZ = False
        #ev_info.isave_ENZ = True

        # EVENT INFO
        # Iceland events 2021-02-24T10:05:57.024000Z -22.20764 63.91658 1.098 5.72
        ev_info.otime = obspy.UTCDateTime("2021-02-24T10:05:57.024000Z")
        ev_info.elon = -22.20764
        ev_info.elat = 63.91658
        ev_info.edep = 1098
        ev_info.emag = 5.72

        ev_info.min_dist = 0
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1000

        #ev_info.network = 'ZB'
        ev_info.channel = 'LH?,BH?,HH?'
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

    elif iex == 1:  # iterate list
        ev_info.overwrite_ddir = 0
        # DATA PREPARATION / PROCESSING
        ev_info.use_catalog = 0
        ev_info.ifmass_downloader = True
        ev_info.ifverbose = True    # output all proccessing steps

        ev_info.icreateNull = 0

        #RAW and ENZ files can be used when checking if you are receiving all the data ($PYSEP/check_getwaveform.bash)
        ev_info.isave_raw = False
        ev_info.isave_raw_processed = False
        ev_info.isave_ENZ = False

        #-----------------------------------------------------------
        # BEGIN ITERATE EVENTS
        inputfile = 'iceland_quake_cat_01-18_Mge4p5'  # 2021-05-12
        #inputfile = 'iceland_quake_cat_01-18_Mge4p5_try2'  # 2021-06-27
        # 2021-02-24T10:05:57.024 -22.20764 63.91658 1.098 5.72 5.13
        # 2021-02-24T10:17:53.076 -22.32224 63.89646 4.862 4.56 4.53
        # 2021-02-24T10:27:59.639 -22.05429 63.91842 3.827 4.70 4.30
        data = np.genfromtxt(inputfile, 
                dtype = (UTCDateTime, float, float, float, float, float), 
                names = "t, lon, lat, dep, mag, ml")
        otime = data['t']
        lon = data['lon']
        lat = data['lat']
        dep = data['dep'] * 1000    # meters
        mag = data['mag']

        ev_info_list = []
        for i, ievid in enumerate(otime):
            print('Processing event %d otime %s' %(i, ievid))
            # template
            iev_info = ev_info.copy()
            iev_info.otime = obspy.UTCDateTime(otime[i])
            iev_info.elon = lon[i]
            iev_info.elat = lat[i]
            iev_info.edep = dep[i] 
            iev_info.emag = mag[i]

            # same requests for all events
            iev_info.min_dist = 0
            iev_info.max_dist = 2000
            iev_info.tbefore_sec = 100
            iev_info.tafter_sec = 1000
            iev_info.channel = 'BH?,HH?'
            iev_info.resample_TF = True
            iev_info.resample_freq = 20
            iev_info.scale_factor = 100

            ev_info_list.append(iev_info)
        # END ITERATE EVENTS
        #-----------------------------------------------------------

        ev_info = ev_info_list
        print(ev_info)

    return(ev_info)
