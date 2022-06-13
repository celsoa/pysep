#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
#

"""

References
St. Gallen
    Earthquakes in Switzerland and surrounding regions during 2013. Swiss J. Geosci., 107, 359-375, doi:10.1007/s00015-014-0171-y.
    Diehl, T., Clinton, J., Kraft, T., Husen, S., Plenkers, K., Guilhem, A., Behr, Y., Cauzzi, C., Kaestli, P., Haslinger, F., Faeh, D., Michel, C., and Wiemer, S., 2014.

Basel
    Full, constrained and stochastic source inversions support evidence for volumetric changes during the Basel earthquake sequence
    Aurélie Guilhem1,2 • Fabian Walter2,3, 2015

20190225 -- cralvizuri <celso.alvizuri@gmail.com>
"""

import obspy
import read_event_obspy_file as reof
from getwaveform import *

def get_ev_info(ev_info,iex):
    ev_info.overwrite_ddir = 0

    # BASEL #  86 (guilhem 2015) 
    ev_info.otime = obspy.UTCDateTime("2006-12-08T03:06:18"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 7.595, 47.585, 4100, 2.6
    # BASEL # 108 (guilhem 2015)
    #ev_info.otime = obspy.UTCDateTime("2006-12-08T16:48:39"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 7.593, 47.584, 4700, 3.4
    # BASEL # 113 (guilhem 2015) - highest ISO
    #ev_info.otime = obspy.UTCDateTime("2006-12-08T20:19:40"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 7.594, 47.583, 4900, 2.5
    # BASEL # 168 (guilhem 2015) 
    #ev_info.otime = obspy.UTCDateTime("2007-01-06T07:19:52"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 7.596, 47.582, 4200, 3.1
    # BASEL # 174 (guilhem 2015)
    #ev_info.otime = obspy.UTCDateTime("2007-01-16T00:09:08"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 7.596, 47.582, 4100, 3.2
    # BASEL # 176 (guilhem 2015) 
    #ev_info.otime = obspy.UTCDateTime("2007-02-02T03:54:28"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 7.596, 47.582, 4000, 3.2

    ## SAINT GALLEN
    #ev_info.otime = obspy.UTCDateTime("2013-07-20T03:30:55"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = 9.316, 47.421, 4000, 3.3

    ## M 5.8 - 14km NW of Pawnee, Oklahoma
    ## https://earthquake.usgs.gov/earthquakes/eventpage/us10006jxs/origin/detail
    #ev_info.otime = obspy.UTCDateTime("2016-09-03 12:02:44.400") 
    #ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = -96.929, 36.425, 5600, 5.8

    # GEYSERS events with large ISO components
    # 2014/01/21 11:11:11.64  38.83933 -122.83850   1.733  3.87   Mw  100  23    0 0.06 NCSN   72144240  ISO -36.9244
    # 2013/10/28 04:59:21.02  38.74483 -122.72234   1.354  3.25   ML   85  22    1 0.06 NCSN   72096866  ISO -35.34455
    # 2011/12/06 01:42:20.31  38.77500 -122.72683   1.119  2.83   Md   91  23    1 0.08 NCSN   71692011  ISO -39.479
    #ev_info.otime = obspy.UTCDateTime("2014-01-21T11:11:11.64"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = -122.83850, 38.83933, 1733, 3.87
    #ev_info.otime = obspy.UTCDateTime("2013-10-28T04:59:21.02"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = -122.72234, 38.74483, 1354, 3.25
    #ev_info.otime = obspy.UTCDateTime("2011-12-06T01:42:20.31"); ev_info.elon, ev_info.elat, ev_info.edep, ev_info.emag = -122.72683, 38.77500, 1119, 2.83

    # BG: geysers, though accelerometers -- see Guilhem 2014 for details on handling
    # NOTE idb default: 1 = IRIS; 2 = AEC; 3 = LLNL; 4 = Geoscope; 5 = CH/ETH
    ev_info.idb = 1; ev_info.network = '*'
    ev_info.idb = 5; ev_info.network = 'CH'
    ev_info.station = '*'
    ev_info.channel = 'BH?,LH?,HH?'
    #ev_info.channel = '*'
    ev_info.use_catalog = 0
    ev_info.min_dist = 0 
    ev_info.max_dist = 500
    ev_info.tbefore_sec = 100
    ev_info.tafter_sec = 2000
    ev_info.scale_factor = 100

    #ev_info.min_lat = 59
    #ev_info.max_lat = 62
    #ev_info.min_lon = -152
    #ev_info.max_lon = -147

    ev_info.resample_freq = 20
    ev_info.ifFilter = True
    ev_info.ipre_filt = 2
    ev_info.filter_type = 'bandpass'
    ev_info.f1 = 1/1000  # fmin
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

    #ev_info.phase_window = False
    #-------for specfem------------
    #ev_info.tbefore_sec = 0
    #ev_info.resample_TF = False
    #ev_info.scale_factor = 1
    #ev_info.outformat = 'DISP'
    #------------------------------

    return(ev_info)
#=================================================================================
# END EXAMPLES
#=================================================================================
