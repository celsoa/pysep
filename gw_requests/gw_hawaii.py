import obspy
#import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    if iex == 0:
        # default list of Alaska networks
        # note 1: cannot use '*' because of IM
        # note 2: may want to exclude the mid-band AV network
        # note 3: these are temporary:
        # XE BEAAR 1999
        # XR ARCTIC 2004
        # XZ STEEP 2005
        # YV MOOS 2006
        # XV FLATS 2014
        # ZE SALMON 2015
        # XG WVF 2016
        # [7C MMEP 2015]
        # TA
        #ev_info.network = 'AK,AT,AV,CN,II,IU,US,XM,XV,XZ,YV'
        #ev_info.network = 'AK' # for testing
        #ev_info.network = 'AK,AT,AV,CN,II,IU,US,XM,TA,XE,XR,XZ,YV,XV,ZE,XG'
        # GCMT search parameters: http://www.globalcmt.org/cgi-bin/globalcmt-cgi-bin/CMT5/form?itype=ymd&yr=2018&mo=6&day=1&otype=ymd&oyr=2018&omo=8&oday=1&jyr=1976&jday=1&ojyr=1976&ojday=1&nday=1&lmw=0&umw=10&lms=0&ums=10&lmb=0&umb=10&llat=19&ulat=20&llon=-156&ulon=-155&lhd=0&uhd=1000&lts=-9999&uts=9999&lpe1=0&upe1=90&lpe2=0&upe2=90&list=6
        # GCMT: -155.07 19.39 12 -1.06 0.52 0.55 0.46 -0.53 0.43 24 X Y 201807181128A
        #ev_info.otime = obspy.UTCDateTime("2018-07-18T11:28:00"); ev_info.elon = -155.07; ev_info.elat = 19.39; ev_info.edep = 12000; ev_info.emag = 5.3
        #ev_info.otime = obspy.UTCDateTime("2018-08-02T21:55:00"); ev_info.elon = -155.09; ev_info.elat = 19.36; ev_info.edep = 12000; ev_info.emag = 5.3
        ev_info.otime = obspy.UTCDateTime("2018-07-18T11:28:04.791000Z"); ev_info.elon = -155.27336; ev_info.elat = 19.40202; ev_info.edep = 1000; ev_info.emag = 5.3

        ev_info.resample_freq = 20
        # ev_info.rlat = 61.45420
        # ev_info.rlon = -149.7428
        # ev_info.rtime = obspy.UTCDateTime("2009-04-07T20:12:55.351")
        ev_info.network = '*,-PN,-XL,-6F'
        ev_info.channel = 'BH?,HH?,HN?,EH?'
        #ev_info.station = '*,-WAID'
        ev_info.station = '*'
        ev_info.use_catalog = 0
        ev_info.idb = 1     # 4 --> ETH
        ev_info.use_catalog = 0
        ev_info.min_dist = 0 
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 2000
        ev_info.scale_factor = 100

        #ev_info.min_lat = 59
        #ev_info.max_lat = 62
        #ev_info.min_lon = -152
        #ev_info.max_lon = -147

        ev_info.ipre_filt = 1
        ev_info.filter_type = 'bandpass'
        ev_info.f1 = 1/1000  # fmin
        ev_info.f2 = 20      # fmax
        ev_info.corners = 4
        ev_info.remove_response = True
        ev_info.demean = True
        ev_info.detrend = True
        ev_info.output_cap_weight_file = True
        #ev_info.outformat = 'DISP'
        ev_info.ifsave_sacpaz = True
        ev_info.overwrite_ddir = 1

        #ev_info.phase_window = False
        #-------for specfem------------
        #ev_info.tbefore_sec = 0
        #ev_info.resample_TF = False
        #ev_info.scale_factor = 1
        #ev_info.outformat = 'DISP'
        #------------------------------
    if iex == 1:
        # LOOP OVER SEVERAL EVENTS
        ev_info.resample_freq = 20
        ev_info.network = '*,-PN,-XL,-6F'
        ev_info.channel = 'BH?,HH?,HN?,EH?'
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
        ev_info.overwrite_ddir = 1

        #ev_info.overwrite_ddir = 1  # use only with evid 201807010051A
        #ev_info.station = '*,-BAKK' # use only with evid 201807010051A

        #inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_gcmt_hi2018'
        # issue with EVID 201807010051A
        # ---> obspy.io.mseed.InternalMSEEDError: Encountered 1 error(s) during a call to readMSEEDBuffer():
        # ---> msr_unpack_data(HV_BAKK_01_HNN_M): only decoded 337 samples of 412 expected

        inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_gcmt_hi2018_x'
        data = np.genfromtxt(inputfile, dtype=None)
        lon = data['f0']
        lat = data['f1']
        dep = data['f2']
        evid = data['f12'].astype(str)

        ev_info_list = []
        for i, ievid in enumerate(evid):
            iev_info = ev_info.copy()
            #print(ievid[:-1])
            # 01234567890123456789
            # |   | | | |
            # 201807010051
            Y = int(ievid[:4])
            M = int(ievid[4:6])
            D = int(ievid[6:8])
            h = int(ievid[8:10])
            m = int(ievid[10:12])
            ot = UTCDateTime(Y, M, D, h, m)
            print(i, ot)
 
            # template
            iev_info.otime = obspy.UTCDateTime(ot)
            iev_info.elon = lon[i]
            iev_info.elat = lat[i]
            iev_info.edep = dep[i] * 1000
            iev_info.emag = -9.99
            ev_info_list.append(iev_info)
        ev_info = ev_info_list
        print(ev_info)
    if iex == 2:
        # LOOP OVER SEVERAL EVENTS
        ev_info.resample_freq = 20
        ev_info.network = '*,-PN,-XL,-6F'
        ev_info.channel = 'BH?,HH?,HN?,EH?' 
        # 2019-04-30 NOTE BAKK has only HN?, no EH, HH, BH. HN? causes issues:
        # obspy.io.mseed.InternalMSEEDError: Encountered 1 error(s) during a call to readMSEEDBuffer():
        # msr_unpack_data(HV_BAKK_01_HNN_M): only decoded 337 samples of 412 expected
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

        #inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_kilauea2018_MAGge4'
        #inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_source/evinfo_kilauea2018_MAGge4redo'
        #inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_source/kilauea2018/evinfo_kilauea2018_MAGge4redo2'
        #inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_catalogs/outcat_hawaii_matched_GCMT_reloc_TEST.txt'   # 2020-01-15 GCMT events but relocated by RM
        #inputfile = '/home/calvizur/REPOSITORIES/geoutils/data_catalogs/outcat_hawaii_matched_GCMT_reloc.txt'   # 2020-01-15 GCMT events but relocated by RM
        #inputfile = 'outcat_hawaii_all_M_ge_5_from_reloc_catalog'      # 2020-07-10 
        inputfile = 'outcat_hawaii_all_M_ge_5_from_reloc_catalog_temp'  # 2020-07-14
        # 2018-05-30T20:53:50.830000Z  -155.2851667 19.4113333      -70.0 5.4  
        # 2018-05-29T11:56:11.570000Z  -155.2828333 19.4123333     -270.0 5.3  
        # 2018-05-29T03:39:36.560000Z  -155.2453333 19.354          930.0 4.12 
        data = np.genfromtxt(inputfile, dtype=(UTCDateTime, float, float, float, float), names="t, lon, lat, dep, mag")

        ## FILE WITH A SINGLE ENTRY
        #otime = [data['t'].tolist().decode('utf-8')] # convert to list to deal with single-row files
        #lon = [data['lon']]
        #lat = [data['lat']]
        #dep = [data['dep']]* 1000
        #mag = [data['mag']]
        ## FILE WITH MULTIPLE ENTRIES
        otime = data['t']
        lon = data['lon']
        lat = data['lat']
        dep = data['dep']* 1000
        mag = data['mag']

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
