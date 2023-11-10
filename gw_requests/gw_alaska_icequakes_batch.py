import obspy
from obspy import UTCDateTime
import read_event_obspy_file as reof
from getwaveform import *
import sys

def get_ev_info(ev_info,iex):
# ===============================================================
# Full list of icequakes since 2000. USGS catalog (derived from Alaska catalog)
# https://earthquake.usgs.gov/earthquakes/map/?currentFeatureId=us7000i3gd&extent=55.72092,219.47388&extent=59.79511,232.25098&range=search&sort=oldest&showUSFaults=true&baseLayer=terrain&timeZone=utc&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%222000-01-01%2000:00:00%22,%22endtime%22:%222022-10-16%2023:59:59%22,%22minmagnitude%22:2.5,%22eventtype%22:%22ice%20quake%22,%22orderby%22:%22time%22%7D%7D
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

    ev_info.min_dist = 0
    ev_info.max_dist = 1000
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 1000

    ev_info.channel = 'LH?,BH?,HH?,SH?'
    ev_info.resample_TF = True
    ev_info.resample_freq = 20
    ev_info.scale_factor = 100

#-----------------------------------------------------------
    #events_file = '/nobackup/celso/REPOSITORIES/geoutils/data_catalogs/icequakes/la'
    events_file = '/nobackup/celso/REPOSITORIES/geoutils/data_catalogs/icequakes/catalog_XGevents_reformatted.dat'
    # 1998-08-18T17:00:19.220  -141.3977   60.0368   2.9000    3.30 G 
    # 2005-09-14T19:59:29.836  -142.9920   60.4384   0.4934    3.70 X 
    # 2005-10-01T22:16:58.341  -140.3120   59.9712   0.0000    3.28 X 

    ev_info_list = []

    data = np.genfromtxt(events_file, dtype=(UTCDateTime,float,float,float,float,str), names="otime, lon, lat, dep, mag, rating")
    otime = [UTCDateTime(t) for t in data['otime']]
    lon = data['lon']
    lat = data['lat']
    dep = data['dep']
    mag = data['mag']

    for i, t in enumerate(otime):
        ev_info = ev_info.copy()    # this is important. else struct+data is overwritten and repeated in the extractions.
        ev_info.otime = t
        ev_info.elon = lon[i] 
        ev_info.elat = lat[i]
        ev_info.edep = dep[i]
        ev_info.emag = mag[i]
        ev_info_list.append(ev_info)

    #la = len(ev_info_list)
    #print(la, ev_info_list)
#-----------------------------------------------------------
    #sys.exit()
        #ev_info.phase_window = False

    return(ev_info_list)
