import obspy
#import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    # LOOP OVER SEVERAL EVENTS
    ev_info.resample_freq = 20
    ev_info.network = '*,-PN,-XL,-6F'
    ev_info.channel = 'BH?,HH?,HN?,EH?' 
    # NOTE HN is Strong Motion accelerometer https://ds.iris.edu/ds/nodes/dmc/tools/data_channels/#HN?
    ev_info.station = '*'
    ev_info.use_catalog = 0
    ev_info.idb = 1
    ev_info.use_catalog = 0
    ev_info.min_dist = 0
    ev_info.max_dist = 2000
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 2000
    ev_info.scale_factor = 100

    ev_info.ipre_filt = 1
    ev_info.filter_type = 'bandpass'
    ev_info.f1 = 1/1000  # fmin
    ev_info.f2 = 20      # fmax
    ev_info.corners = 4
    ev_info.remove_response = True
    ev_info.demean = True
    ev_info.detrend = True
    ev_info.output_cap_weight_file = True
    ev_info.ifsave_sacpaz = True
    ev_info.overwrite_ddir = 0

    inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_jamaica2020.txt'
    data = np.genfromtxt(inputfile, dtype=(UTCDateTime, float, float, float, float), names="t, lon, lat, dep, mag")

    ## FILE WITH A SINGLE ENTRY
    otime = [data['t'].tolist().decode('utf-8')] # convert to list to deal with single-row files
    lon = [data['lon']]
    lat = [data['lat']]
    dep = [data['dep']]* 1000
    mag = [data['mag']]
    ### FILE WITH MULTIPLE ENTRIES
    #otime = data['t']
    #lon = data['lon']
    #lat = data['lat']
    #dep = data['dep']* 1000
    #mag = data['mag']

    ev_info_list = []
    for i, ievid in enumerate(otime):
        print('### test i %d otime %s' %(i, ievid))
        iev_info = ev_info.copy()
        # template
        iev_info.otime = obspy.UTCDateTime(otime[i])
        iev_info.elon = lon[i]
        iev_info.elat = lat[i]
        iev_info.edep = dep[i] 
        iev_info.emag = mag[i]
        ev_info_list.append(iev_info)
    ev_info = ev_info_list
    print(ev_info)

    return(ev_info)
