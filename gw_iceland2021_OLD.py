#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""
try get waveforms seismic events iceland

https://earthquake.usgs.gov/earthquakes/map/?currentFeatureId=us6000dkmk&extent=63.62064,-23.48602&extent=64.69676,-20.13794&range=search&sort=largest&timeZone=utc&search=%7B%22name%22:%22Search%20Results%22,%22params%22:%7B%22starttime%22:%222020-12-01%2000:00:00%22,%22endtime%22:%222021-03-25%2023:59:59%22,%22maxlatitude%22:67.002,%22minlatitude%22:62.678,%22maxlongitude%22:-12.195,%22minlongitude%22:-25.159,%22minmagnitude%22:4,%22orderby%22:%22time%22%7D%7D

Latest: https://earthquake.usgs.gov/earthquakes/eventpage/us6000dkmk/executive
    M 5.6 - 6 km SE of Vogar, Iceland
    2021-02-24 10:05:59 (UTC)63.949°N 22.285°W

20210325 -- cralvizuri <celso.alvizuri@gmail.com>
"""

#import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    if iex == 1:
        ev_info.idb = 99
        ev_info.use_catalog = 0
        #2021-02-24T10:05:57.024000Z -22.20764 63.91658 1.098 5.72
        ev_info.otime = obspy.UTCDateTime("2021-02-24T10:05:57.024000Z")
        ev_info.elon = -22.20764
        ev_info.elat = 63.91658
        ev_info.edep = 1098 
        ev_info.min_dist = 0
        ev_info.max_dist = 1000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 300

        #output all proccessing steps
        ev_info.ifverbose = True

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


        ev_info.channel = 'BH?'
        ev_info.use_catalog = 0
        # ev_info.rlat = 61.45420
        # ev_info.rlon = -149.7428
        # ev_info.rtime = obspy.UTCDateTime("2009-04-07T20:12:55.351")
        ev_info.emag = 4.6
        ev_info.resample_freq = 50
        ev_info.scale_factor = 100
    elif iex == 2:
        ev_info.idb = 99
        # LOOP OVER SEVERAL EVENTS
        ev_info.resample_freq = 20
        #ev_info.network = '2C,3P,9H,AM,II,VI,YG,ZB,GFZ,CH'
        #ev_info.network = '*'
        #ev_info.network = 'GFZ'
        ev_info.channel = 'BH?,HH?,HN?,EH?' 
        #ev_info.channel = 'BHZ' 
        # 2019-04-30 NOTE BAKK has only HN?, no EH, HH, BH. HN? causes issues:
        # obspy.io.mseed.InternalMSEEDError: Encountered 1 error(s) during a call to readMSEEDBuffer():
        # msr_unpack_data(HV_BAKK_01_HNN_M): only decoded 337 samples of 412 expected
        # NOTE HN is Strong Motion accelerometer https://ds.iris.edu/ds/nodes/dmc/tools/data_channels/#HN?
        ev_info.station = '*'
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
        ev_info.overwrite_ddir = False

        #inputfile = 'outcat_hawaii_all_M_ge_5_from_reloc_catalog_temp'  # 2020-07-14
        #inputfile = 'query_usgs_iceland2021_clean.csv'
        inputfile = 'iceland_quake_cat_01-18_largest'
        inputfile = 'iceland_quake_cat_01-18_s-L'
        data = np.genfromtxt(inputfile, dtype=(UTCDateTime, float, float, float, float), names="t, lon, lat, dep, mag")

        ## FILE WITH A SINGLE ENTRY
        #otime = [data['t'].tolist().decode('utf-8')] # convert to list to deal with single-row files
        #lon = [data['lon']]
        #lat = [data['lat']]
        #dep = [data['dep']]* 1000
        #mag = [data['mag']]
        # FILE WITH MULTIPLE ENTRIES
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
        print('DEBUG gw_iceland2021.py')
        print(ev_info)

    elif iex == 3:
        ev_info.idb = 1
 
        # https://earthquake.usgs.gov/earthquakes/eventpage/us70008jr5
        ev_info.use_catalog = 0
        # 2021-04-06. test sampling 0.01.  event 2021-03-14T14:15:26.689Z -22.138  64.039  10000 5.3
        # 2021-04-06. NOTE need to redo the following, I overwrote by mistake.  2021-03-14T14:15. 26.689Z -22.138  64.039  10000 5.3
        ev_info.otime = obspy.UTCDateTime('2021-03-14T14:15:26.689Z') #  -22.138  64.039  10000 5.3
        ev_info.elon = -22.138
        ev_info.elat = 64.039
        ev_info.edep = 10000
        ev_info.emag = 5.3
        ev_info.min_dist = 0 
        ev_info.max_dist = 2000
        ev_info.tbefore_sec = 100
        ev_info.tafter_sec = 1000

        ev_info.ifFilter = True
        ev_info.ipre_filt = 2
        ev_info.filter_type = 'bandpass'
        #ev_info.f1 = 1/1000  # orig
        ev_info.f1 = 1/2000  # try 2 (2020-02-04)
        ev_info.f2 = 20      # fmax
        ev_info.corners = 4
        ev_info.remove_response = True
        ev_info.demean = True
        ev_info.detrend = True
        ev_info.output_cap_weight_file = True
        # ev_info.outformat = 'DISP'
        ev_info.ifsave_sacpaz = True
        ev_info.isave_raw = True
        #ev_info.ifverbose = False

        ev_info.network = '*,-PN,-XL,-6F'
        #ev_info.channel = 'LH?,BH?,HH?'
        ev_info.channel = 'BH?,HH?'
        ev_info.use_catalog = 0
        ev_info.resample_freq = 100 # NOTE 2021-04-06. test with 0.01 greens functions.
        ev_info.resample_freq = 20 # NOTE 2021-04-06. test with 0.01 greens functions.
        ev_info.scale_factor = 100
        ev_info.overwrite_ddir = 1
    else:
        print('option iex %d\n', iex);


    return(ev_info)